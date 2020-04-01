/**
 * Copyright (c) 2010-2020 Contributors to the openHAB project
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0
 *
 * SPDX-License-Identifier: EPL-2.0
 */
package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import java.nio.ByteBuffer;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import org.eclipse.jdt.annotation.NonNull;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.jetty.client.HttpClient;
import org.eclipse.jetty.client.api.Response;
import org.eclipse.jetty.client.api.Result;
import org.eclipse.jetty.client.util.BufferingResponseListener;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants;
import org.eclipse.smarthome.core.thing.binding.firmware.Firmware;
import org.eclipse.smarthome.core.thing.binding.firmware.ProgressCallback;

public class FlashUtils {
    public static byte @Nullable [] downloadFirmware(@NonNull Firmware firmware, @NonNull ProgressCallback progressCallback, @NonNull HttpClient httpClient) {
        String url = firmware.getProperties().getOrDefault(TinkerforgeBindingConstants.PROPERTY_FIRMWARE_URL, "");
        if (url == "") {
            progressCallback.failed("Failed to update: firmware download URL missing");
            return null;
        }
        ArrayBlockingQueue<byte[]> queue = new ArrayBlockingQueue<>(1);
        AtomicInteger contentLength = new AtomicInteger(-1);

        httpClient.newRequest(url).send(new BufferingResponseListener() {
            @Override
            public void onHeaders(Response response) {
                super.onHeaders(response);
                if (response.getHeaders().containsKey("Content-Length")) {
                    try {
                        contentLength.set(Integer.parseInt(response.getHeaders().getField("Content-Length").getValue()));
                    } catch (NumberFormatException e) {
                    }
                }
            }

            @Override
            public void onContent(Response response, ByteBuffer content) {
                int cLength = contentLength.get();
                if (cLength > 0) {
                    double have = (cLength - content.remaining()) / ((double) cLength);
                    progressCallback.update((int) (have / 4 * 100));
                }
                super.onContent(response, content);
            }

            @Override
            public void onComplete(Result result) {
                if (result.isSucceeded()) {
                    try {
                        queue.put(getContent());
                    } catch (InterruptedException e) {
                        progressCallback
                                .failed("Failed to download firmware: interrupted while putting firmware in the result queue.");
                    }
                } else {
                    progressCallback.failed("Failed to download firmware: {}", result.getFailure().toString());
                }
            }
        });

        byte[] plugin;
        try {
            plugin = queue.poll(1, TimeUnit.MINUTES);
        } catch (InterruptedException e1) {
            progressCallback
                    .failed("Failed to download firmware: interrupted while waiting for firmware result queue.");
            return null;
        }
        return plugin;
    }
}
