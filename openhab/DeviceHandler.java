/**
 * Copyright (c) 2014,2019 Contributors to the Eclipse Foundation
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0
 *
 * SPDX-License-Identifier: EPL-2.0
 */
package org.eclipse.smarthome.binding.tinkerforge.internal.handler;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.jetty.client.HttpClient;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeChannelTypeProvider;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeThingTypeProvider;
import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter;
import org.eclipse.smarthome.config.core.ConfigDescriptionRegistry;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type;
import org.eclipse.smarthome.core.thing.Bridge;
import org.eclipse.smarthome.core.thing.Channel;
import org.eclipse.smarthome.core.thing.ChannelUID;
import org.eclipse.smarthome.core.thing.Thing;
import org.eclipse.smarthome.core.thing.ThingStatus;
import org.eclipse.smarthome.core.thing.ThingStatusDetail;
import org.eclipse.smarthome.core.thing.ThingStatusInfo;
import org.eclipse.smarthome.core.thing.binding.BaseThingHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.eclipse.smarthome.core.thing.binding.ThingHandlerService;
import org.eclipse.smarthome.core.thing.binding.builder.ChannelBuilder;
import org.eclipse.smarthome.core.thing.binding.firmware.Firmware;
import org.eclipse.smarthome.core.thing.binding.firmware.FirmwareUpdateHandler;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressCallback;
import org.eclipse.smarthome.core.thing.type.ChannelDefinition;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeRegistry;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.RefreshType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.net.URI;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.function.BiFunction;
import java.util.function.Supplier;

import com.tinkerforge.BrickMaster;
import com.tinkerforge.IPConnection;
import com.tinkerforge.TinkerforgeException;
import com.tinkerforge.Device.Identity;

import org.eclipse.smarthome.binding.tinkerforge.internal.device.CoMCUFlashable;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapper;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapperFactory;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.StandardFlashHost;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.StandardFlashable;
import org.eclipse.smarthome.binding.tinkerforge.internal.device.DeviceWrapper.SetterRefresh;
import com.tinkerforge.IPConnection.EnumerateListener;

/**
 * The {@link DeviceHandler} is responsible for handling commands, which are
 * sent to one of the channels.
 *
 * @author Erik Fleckstein - Initial contribution
 */
@NonNullByDefault
public class DeviceHandler extends BaseThingHandler implements FirmwareUpdateHandler {
    private final Logger logger = LoggerFactory.getLogger(DeviceHandler.class);

    private boolean wasInitialized = false;

    @Nullable
    private DeviceWrapper device;

    private final BiFunction<String, IPConnection, DeviceWrapper> deviceSupplier;

    private Class<? extends ThingHandlerService> actionsClass;

    private Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier;
    private Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier;
    private @Nullable EnumerateListener enumerateListener;
    private @Nullable HttpClient httpClient;

    public DeviceHandler(Thing thing, BiFunction<String, IPConnection, DeviceWrapper> deviceSupplier,
            Class<? extends ThingHandlerService> actionsClass,
            Supplier<ChannelTypeRegistry> channelTypeRegistrySupplier,
            Supplier<ConfigDescriptionRegistry> configDescriptionRegistrySupplier, @Nullable HttpClient httpClient) {
        super(thing);

        this.deviceSupplier = deviceSupplier;
        this.actionsClass = actionsClass;
        this.channelTypeRegistrySupplier = channelTypeRegistrySupplier;
        this.configDescriptionRegistrySupplier = configDescriptionRegistrySupplier;
        this.httpClient = httpClient;
    }

    public @Nullable DeviceWrapper getDevice() {
        return device;
    }

    public boolean checkReachablity() {
        try {
            logger.debug("Checking reachability of {}", thing.getUID().getId());
            Identity id = getDevice().getIdentity();
            String fwVersion = id.firmwareVersion[0] + "." + id.firmwareVersion[1] + "." + id.firmwareVersion[2];
            this.getThing().setProperty(Thing.PROPERTY_FIRMWARE_VERSION, fwVersion);
            logger.debug("Done checking reachability of {}", thing.getUID().getId());

            // Initialize will set the status itself if the configuration succeeds.
            if (!thing.getStatus().equals(ThingStatus.ONLINE))
                initializeDevice();
            return true;
        } catch (TinkerforgeException e) {
            logger.debug("Failed checking reachability of {}: {}", thing.getUID().getId(), e.getMessage());
            return false;
        }
    }

    public void reachabilityCheckFailed() {
        updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.COMMUNICATION_ERROR, "Device is unreachable.");
    }

    private void enumerateListener(String uid, String connectedUid, char position, short[] hardwareVersion,
            short[] firmwareVersion, int deviceIdentifier, short enumerationType) {
        String id = thing.getUID().getId();

        if (!uid.equals(id)) {
            return;
        }

        if (enumerationType == IPConnection.ENUMERATION_TYPE_DISCONNECTED) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.NONE, "Device was unplugged.");
            return;
        }
        String fwVersion = firmwareVersion[0] + "." + firmwareVersion[1] + "." + firmwareVersion[2];
        this.getThing().setProperty(Thing.PROPERTY_FIRMWARE_VERSION, fwVersion);

        if (enumerationType == IPConnection.ENUMERATION_TYPE_CONNECTED) {
            initializeDevice();
        }
    }

    @Override
    public void initialize() {
        if (getBridge() == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.CONFIGURATION_ERROR, "Bridge not found.");
            return;
        }

        BrickDaemonHandler brickd = (BrickDaemonHandler) (getBridge().getHandler());
        if (!wasInitialized) {
            enumerateListener = this::enumerateListener;
            brickd.addEnumerateListener(enumerateListener);
        }
        wasInitialized = true;

        com.tinkerforge.IPConnection ipcon = brickd.ipcon;

        String id = thing.getUID().getId();
        if (device != null)
            device.cancelManualUpdates();
        device = deviceSupplier.apply(id, ipcon);

        configureChannels();

        if (this.getBridge().getStatus() == ThingStatus.ONLINE) {
            initializeDevice();
        } else {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
        }
    }

    private Configuration getChannelConfiguration(String channelID) {
        return getThing().getChannel(channelID).getConfiguration();
    }

    protected void initializeDevice() {
        String id = thing.getUID().getId();
        Bridge bridge = getBridge();
        if (bridge == null) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_UNINITIALIZED);
            return;
        }
        BrickDaemonHandler brickd = (BrickDaemonHandler) (bridge.getHandler());
        com.tinkerforge.IPConnection ipcon = brickd.ipcon;
        if (device != null)
            device.cancelManualUpdates();
        device = deviceSupplier.apply(id, ipcon);

        try {
            device.initialize(getConfig(), this::getChannelConfiguration, this::updateState, this::triggerChannel,
                    scheduler, this);
        } catch (TinkerforgeException e) {
            brickd.handleTimeout(this);
            return;
        }
        updateStatus(ThingStatus.ONLINE, ThingStatusDetail.NONE);

        this.getThing().getChannels().stream().filter(c -> !c.getChannelTypeUID().toString().startsWith("system"))
                .forEach(c -> handleCommand(c.getUID(), RefreshType.REFRESH));
    }

    @Override
    public void bridgeStatusChanged(ThingStatusInfo bridgeStatusInfo) {
        if (bridgeStatusInfo.getStatus() == ThingStatus.ONLINE) {
            initializeDevice();
        } else if (bridgeStatusInfo.getStatus() == ThingStatus.OFFLINE) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.BRIDGE_OFFLINE);
        }
    }

    private void refreshValue(String channelId, Configuration channelConfig) {
        try {
            device.refreshValue(channelId, getConfig(), channelConfig, this::updateState, this::triggerChannel);
        } catch (TinkerforgeException e) {
            ((BrickDaemonHandler) (getBridge().getHandler())).handleTimeout(this);
        }
    }

    @Override
    public void handleCommand(ChannelUID channelUID, Command command) {
        if (this.getBridge() == null || this.getBridge().getStatus() == ThingStatus.OFFLINE) {
            return;
        }

        try {
            if (command instanceof RefreshType) {
                refreshValue(channelUID.getId(), getThing().getChannel(channelUID).getConfiguration());
            } else {
                List<SetterRefresh> refreshs = device.handleCommand(getConfig(),
                        getThing().getChannel(channelUID).getConfiguration(), channelUID.getId(), command);
                refreshs.forEach(r -> scheduler.schedule(
                        () -> refreshValue(r.channel, getThing().getChannel(r.channel).getConfiguration()), r.delay,
                        TimeUnit.MILLISECONDS));
            }
        } catch (TinkerforgeException e) {
            ((BrickDaemonHandler) (getBridge().getHandler())).handleTimeout(this);
        }
    }

    @Override
    public void handleRemoval() {
        try {
            if (device != null) {
                device.cancelManualUpdates();
                BrickDaemonHandler brickd = (BrickDaemonHandler) (getBridge().getHandler());
                if (brickd != null)
                    brickd.removeEnumerateListener(enumerateListener);
                device.dispose(getConfig());
            }

        } catch (TinkerforgeException e) {
        }
        updateStatus(ThingStatus.REMOVED);
    }

    private Channel buildChannel(ThingType tt, ChannelDefinition def) {
        ChannelType ct = TinkerforgeChannelTypeProvider.getChannelTypeStatic(def.getChannelTypeUID(), null);
        if (ct == null) {
            ChannelTypeRegistry reg = channelTypeRegistrySupplier.get();
            if (reg == null) {
                logger.warn("Could not get build channel {}: ChannelTypeRegistry not found.", def.getId());
                return null;
            }
            ct = reg.getChannelType(def.getChannelTypeUID());
        }
        ChannelBuilder builder = ChannelBuilder
                .create(new ChannelUID(getThing().getUID(), def.getId()), ct.getItemType())
                .withAutoUpdatePolicy(def.getAutoUpdatePolicy()).withProperties(def.getProperties())
                .withType(def.getChannelTypeUID()).withKind(ct.getKind());

        String desc = def.getDescription();
        if (desc != null) {
            builder = builder.withDescription(desc);
        }
        String label = def.getLabel();
        if (label != null) {
            builder = builder.withLabel(label);
        }

        // Initialize channel configuration with default-values
        URI confDescURI = ct.getConfigDescriptionURI();
        ConfigDescriptionRegistry reg = configDescriptionRegistrySupplier.get();
        if (reg == null || confDescURI == null) {
            return builder.build();
        }

        ConfigDescription cd = reg.getConfigDescription(confDescURI);
        if (cd == null) {
            return builder.build();
        }

        Configuration config = new Configuration();
        for (ConfigDescriptionParameter param : cd.getParameters()) {
            String defaultValue = param.getDefault();
            if (defaultValue == null) {
                continue;
            }

            Object value = getDefaultValueAsCorrectType(param.getType(), defaultValue);
            if (value == null) {
                continue;
            }

            config.put(param.getName(), value);
        }
        builder = builder.withConfiguration(config);

        return builder.build();
    }

    public @Nullable Object getDefaultValueAsCorrectType(Type parameterType, String defaultValue) {
        try {
            switch (parameterType) {
            case TEXT:
                return defaultValue;
            case BOOLEAN:
                return Boolean.parseBoolean(defaultValue);
            case INTEGER:
                return new BigDecimal(defaultValue);
            case DECIMAL:
                return new BigDecimal(defaultValue);
            default:
                return null;
            }
        } catch (NumberFormatException ex) {
            logger.warn("Could not parse default value '{}' as type '{}': {}", defaultValue, parameterType,
                    ex.getMessage(), ex);
            return null;
        }
    }

    private void configureChannels() {
        List<String> enabledChannelNames = new ArrayList<>();
        try {
            enabledChannelNames = device.getEnabledChannels(getConfig());
        } catch (TinkerforgeException e) {
            ((BrickDaemonHandler) (getBridge().getHandler())).handleTimeout(this);
        }

        ThingType tt = TinkerforgeThingTypeProvider.getThingTypeStatic(this.getThing().getThingTypeUID(), null);

        List<Channel> enabledChannels = new ArrayList<>();
        for (String s : enabledChannelNames) {
            ChannelUID cuid = new ChannelUID(getThing().getUID(), s);
            ChannelDefinition def = tt.getChannelDefinitions().stream().filter(d -> d.getId().equals(cuid.getId()))
                    .findFirst().get();
            Channel newChannel = buildChannel(tt, def);

            Channel existingChannel = this.thing.getChannel(newChannel.getUID());
            if (existingChannel != null)
                newChannel = ChannelBuilder.create(newChannel).withConfiguration(existingChannel.getConfiguration())
                        .build();

            enabledChannels.add(newChannel);
        }

        updateThing(editThing().withChannels(enabledChannels).build());
    }

    @Override
    public Collection<Class<? extends ThingHandlerService>> getServices() {
        return Collections.singletonList(actionsClass);
    }

    @Override
    public void updateFirmware(Firmware firmware, ProgressCallback progressCallback) {
        if (this.device instanceof CoMCUFlashable) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.FIRMWARE_UPDATING, "Firmware is updating");

            CoMCUFlashable flashable = (CoMCUFlashable) this.device;
            flashable.flash(firmware, progressCallback, this.httpClient);

            updateStatus(ThingStatus.ONLINE);
            return;
        }

        if (this.device instanceof StandardFlashable) {
            updateStatus(ThingStatus.OFFLINE, ThingStatusDetail.FIRMWARE_UPDATING, "Firmware is updating");

            Identity id;
            try {
                id = this.device.getIdentity();
            } catch (TinkerforgeException e) {
                progressCallback.failed("Failed to get device identity: {}", e.getMessage());
                ((BrickDaemonHandler) (getBridge().getHandler())).handleTimeout(this);
                return;
            }
            String hostUID = id.connectedUid;

            ThingHandler hostHandler = ((BrickDaemonHandler) getBridge().getHandler()).getChildHandler(hostUID);

            DeviceWrapper hostDevice;
            if (hostHandler != null)
                hostDevice = ((DeviceHandler) hostHandler).getDevice();
            else {
                IPConnection ipcon = ((BrickDaemonHandler) getBridge().getHandler()).ipcon;
                Identity hostId;
                try {
                    hostId = new BrickMaster(hostUID, ipcon).getIdentity();
                } catch (TinkerforgeException e) {
                    progressCallback.failed("Failed to get host identity: {}", e.getMessage());
                    ((BrickDaemonHandler) (getBridge().getHandler())).handleTimeout(this);
                    return;
                }
                try {
                    hostDevice = DeviceWrapperFactory.createDevice(hostId.deviceIdentifier, hostUID, ipcon);
                } catch (Exception e) {
                    progressCallback.failed("Failed to create host device wrapper: {}", e.getMessage());
                    return;
                }
            }

            if (!(hostDevice instanceof StandardFlashHost)) {
                progressCallback.failed("Device is connected to host that does not implement StandardFlashHost");
                return;
            }

            ((StandardFlashHost)hostDevice).flash(id.position, firmware, progressCallback, httpClient);
        }
    }

    @Override
    public void cancel() {
        // not needed for now
    }

    @Override
    public boolean isUpdateExecutable() {
        return this.httpClient != null && (this.device instanceof CoMCUFlashable || this.device instanceof StandardFlashable);
    }
}
