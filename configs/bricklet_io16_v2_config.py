# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# IO-16 Bricklet 2.0 communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2114,
    'name': 'IO16 V2',
    'display_name': 'IO-16 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '16-channel digital input/output',
        'de': '16 digitale Ein- und Ausgänge'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Direction',
'type': 'char',
'constants': [('In', 'i'),
              ('Out', 'o')]
})

com['constant_groups'].append({
'name': 'Edge Type',
'type': 'uint8',
'constants': [('Rising', 0),
              ('Falling', 1),
              ('Both', 2)]
})

com['doc'] = {
'en':
"""
The Bricklet has sixteen channels that are named 0 to 15 in the API. The
corresponding connectors on the Bricklet are labeled A0 to A7 for channel 0 to 7
and B0 to B7 for channels 8 to 15.
""",
'de':
"""
Das Bricklet hat sechzehn Kanäle die in der API von 0 bis 15 benannt sind. Die
entsprechenden Anschlüsse auf dem Bricklet sind mit A0 bis A7 für die Kanäle 0
bis 7 und B0 bis B7 für die Kanäle 8 bis 15 benannt.
"""
}

com['packets'].append({
'type': 'function',
'name': 'Set Value',
'elements': [('Value', 'bool', 16, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value of all sixteen channels. A value of *true* or *false* outputs
logic 1 or logic 0 respectively on the corresponding channel.

Use :func:`Set Selected Value` to change only one output channel state.

For example: (True, True, False, False, ..., False) will turn the channels 0-1
high and the channels 2-15 low.

All running monoflop timers will be aborted if this function is called.

.. note::
 This function does nothing for channels that are configured as input. Pull-up
 resistors can be switched on with :func:`Set Configuration`.
""",
'de':
"""
Setzt den Zustand aller sechzehn Kanäle. Der Wert *true* bzw. *false* erzeugen
logisch 1 bzw. logisch 0 auf dem entsprechenden Kanal.

Mittels :func:`Set Selected Value` können auch einzelnen Kanäle gesetzt werden.

Beispiel: (True, True, False, False, ..., False) setzt die Kanäle 0-1 auf logisch 1 und die
Kanäle 2-15 auf logisch 0.

Alle laufenden Monoflop Timer werden abgebrochen, wenn diese Funktion
aufgerufen wird.

.. note::
 Diese Funktion bewirkt keine Änderung an Kanälen die als Eingang konfiguriert
 sind. Pull-Up Widerstände können mit :func:`Set Configuration` zugeschaltet
 werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Value',
'elements': [('Value', 'bool', 16, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the logic levels that are currently measured on the channels.
This function works if the channel is configured as input as well as if it is
configured as output.
""",
'de':
"""
Gibt die aktuell gemessenen Zustände zurück. Diese Funktion gibt die Zustände
aller Kanäle zurück, unabhängig ob diese als Ein- oder Ausgang konfiguriert
sind.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Selected Value',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Value', 'bool', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the output value of a specific channel without affecting the other channels.

A running monoflop timer for the specific channel will be aborted if this
function is called.

.. note::
 This function does nothing for channels that are configured as input. Pull-up
 resistors can be switched on with :func:`Set Configuration`.
""",
'de':
"""
Setzt den Ausgabewert des ausgewählten Kanals ohne die anderen Kanäle zu
beeinflussen.

Ein laufender Monoflop Timer für den ausgewählten Kanal wird abgebrochen,
wenn diese Funktion aufgerufen wird.

.. note::
 Diese Funktion bewirkt keine Änderung an Kanälen die als Eingang konfiguriert
 sind. Pull-Up Widerstände können mit :func:`Set Configuration` zugeschaltet
 werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Direction', 'char', 1, 'in', {'constant_group': 'Direction', 'default': 'i'}),
             ('Value', 'bool', 1, 'in', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Configures the value and direction of a specific channel. Possible directions
are 'i' and 'o' for input and output.

If the direction is configured as output, the value is either high or low
(set as *true* or *false*).

If the direction is configured as input, the value is either pull-up or
default (set as *true* or *false*).

For example:

* (0, 'i', true) will set channel-0 as input pull-up.
* (1, 'i', false) will set channel-1 as input default (floating if nothing is connected).
* (2, 'o', true) will set channel-2 as output high.
* (3, 'o', false) will set channel-3 as output low.

A running monoflop timer for the specific channel will be aborted if this
function is called.
""",
'de':
"""
Konfiguriert den Zustand und die Richtung eines angegebenen Kanals. Mögliche
Richtungen sind 'i' und 'o' für Ein- und Ausgang.

Wenn die Richtung als Ausgang konfiguriert ist, ist der Zustand entweder
logisch 1 oder logisch 0 (gesetzt als *true* oder *false*).

Wenn die Richtung als Eingang konfiguriert ist, ist der Zustand entweder
Pull-Up oder Standard (gesetzt als *true* oder *false*).

Beispiele:

* (0, 'i', true) setzt Kanal-0 als Eingang mit Pull-Up.
* (1, 'i', false) setzt Kanal-1 als Standard Eingang (potentialfrei wenn nicht verbunden).
* (2, 'o', true) setzt Kanal-2 als Ausgang im Zustand logisch 1.
* (3, 'o', false) setzt Kanal-3 als Ausgang im Zustand logisch 0.

Ein laufender Monoflop Timer für den angegebenen Kanal wird abgebrochen,
wenn diese Funktion aufgerufen wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Direction', 'char', 1, 'out', {'constant_group': 'Direction', 'default': 'i'}),
             ('Value', 'bool', 1, 'out', {'default': True})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the channel configuration as set by :func:`Set Configuration`.
""",
'de':
"""
Gibt die Kanal-Konfiguration zurück, wie von :func:`Set Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Input Value Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
This callback can be configured per channel.

The period is the period with which the :cb:`Input Value`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Dieser Callback kann pro Kanal konfiguriert werden.

Die Periode ist die Periode mit der der :cb:`Input Value`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Input Value Callback Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Input Value Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Input Value Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set All Input Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`All Input Value`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`All Input Value`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Input Value Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set All Input Value Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set All Input Value Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Monoflop',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Value', 'bool', 1, 'in', {}),
             ('Time', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures a monoflop of the specified channel.

The second parameter is the desired value of the specified
channel. A *true* means relay closed and a *false* means relay open.

The third parameter indicates the time that the channels should hold
the value.

If this function is called with the parameters (0, 1, 1500) channel 0 will
close and in 1.5s channel 0 will open again

A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
have a RS485 bus and a IO-16 Bricklet 2.0 connected to one of
the slave stacks. You can now call this function every second, with a time
parameter of two seconds and channel 0 closed. Channel 0 will be closed all the
time. If now the RS485 connection is lost, then channel 0 will be opened in at
most two seconds.
""",
'de':
"""
Konfiguriert einen Monoflop für den angegebenen Kanal.

Der zweite Parameter ist eine der gewünschten Zustände des
festgelegten Kanals. Eine *true bedeutet Relais geschlossen und
ein *false* bedeutet Relais offen.

Der dritte Parameter ist die Zeit die der Kanal den Zustand
halten sollen.

Wenn diese Funktion mit den Parametern (0, 1, 1500) aufgerufen wird,
wird Kanal 0 geschlossen und nach 1,5s wieder geöffnet.

Ein Monoflop kann zur Ausfallsicherung verwendet werden. Beispiel:
Angenommen ein RS485 Bus und ein IO-16 Bricklet 2.0 ist an ein
Slave Stapel verbunden.
Jetzt kann diese Funktion sekündlich, mit einem Zeitparameter von 2 Sekunden,
aufgerufen werden. Der Kanal wird die gesamte Zeit im Zustand geschlossen sein.
Wenn jetzt die RS485 Verbindung getrennt wird, wird der Kanal nach spätestens
zwei Sekunden in den Zustand geöffnet wechseln.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Monoflop',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Value', 'bool', 1, 'out', {}),
             ('Time', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Time Remaining', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns (for the given channel) the current value and the time as set by
:func:`Set Monoflop` as well as the remaining time until the value flips.

If the timer is not running currently, the remaining time will be returned
as 0.
""",
'de':
"""
Gibt (für den angegebenen Kanal) den aktuellen Zustand und die Zeit, wie von
:func:`Set Monoflop` gesetzt, sowie die noch verbleibende Zeit bis zum
Zustandswechsel, zurück.

Wenn der Timer aktuell nicht läuft, ist die noch verbleibende Zeit 0.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Reset Counter', 'bool', 1, 'in', {}),
             ('Count', 'uint32', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the current value of the edge counter for the selected channel. You can
configure the edges that are counted with :func:`Set Edge Count Configuration`.

If you set the reset counter to *true*, the count is set back to 0
directly after it is read.
""",
'de':
"""
Gibt den aktuellen Wert des Flankenzählers für den ausgewählten Kanal zurück. Die
zu zählenden Flanken können mit :func:`Set Edge Count Configuration` konfiguriert werden.

Wenn `reset counter` auf *true* gesetzt wird, wird der Zählerstand direkt
nach dem auslesen auf 0 zurückgesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Edge Count Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Edge Type', 'uint8', 1, 'in', {'constant_group': 'Edge Type', 'default': 0}),
             ('Debounce', 'uint8', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Configures the edge counter for a specific channel.

The edge type parameter configures if rising edges, falling edges or
both are counted if the channel is configured for input. Possible edge types are:

* 0 = rising
* 1 = falling
* 2 = both

Configuring an edge counter resets its value to 0.

If you don't know what any of this means, just leave it at default. The
default configuration is very likely OK for you.
""",
'de':
"""
Konfiguriert den Flankenzähler für einen bestimmten Kanal.

Der edge type Parameter konfiguriert den zu zählenden Flankentyp. Es können
steigende, fallende oder beide Flanken gezählt werden für Kanäle die als Eingang
konfiguriert sind. Mögliche Flankentypen sind:

* 0 = steigend
* 1 = fallend
* 2 = beide

Durch das Konfigurieren wird der Wert des Flankenzählers auf 0 zurückgesetzt.

Falls unklar ist was dies alles bedeutet, kann diese Funktion einfach
ignoriert werden. Die Standardwerte sind in fast allen Situationen OK.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Edge Count Configuration',
'elements': [('Channel', 'uint8', 1, 'in', {'range': (0, 15)}),
             ('Edge Type', 'uint8', 1, 'out', {'constant_group': 'Edge Type', 'default': 0}),
             ('Debounce', 'uint8', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 100})],
'since_firmware': [1, 0, 0],
'doc': ['af', {
'en':
"""
Returns the edge type and debounce time for the selected channel as set by
:func:`Set Edge Count Configuration`.
""",
'de':
"""
Gibt den Flankentyp sowie die Entprellzeit für den ausgewählten Kanals zurück,
wie von :func:`Set Edge Count Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Input Value',
'elements': [('Channel', 'uint8', 1, 'out', {'range': (0, 15)}),
             ('Changed', 'bool', 1, 'out', {}),
             ('Value', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Input Value Callback Configuration`.

The parameters are the channel, a value-changed indicator and the actual value
for the channel. The `changed` parameter is true if the value has changed since
the last callback.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Input Value Callback Configuration` gesetzten Konfiguration

Die Parameter sind der Kanal, Changed und der Wert. Der `changed`-Parameter
ist True wenn sich der Wert seit dem letzten Callback geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'All Input Value',
'elements': [('Changed', 'bool', 16, 'out', {}),
             ('Value', 'bool', 16, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set All Input Value Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Value`. Additional the
`changed` parameter is true if the value has changed since
the last callback.

""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set All Input Value Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get Value`. Zusätzlich ist der
`changed`-Parameter True wenn sich der Wert seit dem letzten Callback geändert hat.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Monoflop Done',
'elements': [('Channel', 'uint8', 1, 'out', {'range': (0, 15)}),
             ('Value', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a monoflop timer reaches 0. The
:word:`parameters` contain the channel and the current value of the channel
(the value after the monoflop).
""",
'de':
"""
Dieser Callback wird ausgelöst, wenn ein Monoflop Timer abläuft (0 erreicht).
:word:`parameters` enthalten den Kanal und den aktuellen Zustand des Kanals
(der Zustand nach dem Monoflop).
"""
}]
})

com['examples'].append({
'name': 'Output',
'functions': [('setter', 'Set Configuration', [('uint8', 7), ('char', 'o'), ('bool', False)], 'Configure channel 7 as output low', None),
              ('loop_header', 10, 'Set channel 7 alternating high/low 10 times with 100 ms delay'),
              ('sleep', 100, None, None),
              ('setter', 'Set Selected Value', [('uint8', 7), ('bool', True)], None, None),
              ('sleep', 100, None, None),
              ('setter', 'Set Selected Value', [('uint8', 7), ('bool', False)], None, None),
              ('loop_footer',)]
})

com['examples'].append({
'name': 'Interrupt',
'functions': [('callback', ('Input Value', 'input value'), [(('Channel', 'Channel'), 'uint8', 1, None, None, None), (('Changed', 'Changed'), 'bool', 1, None, None, None), (('Value', 'Value'), 'bool', 1, None, None, None)], None, None),
              ('callback_configuration', ('Input Value', 'input value (channel 4)'), [('uint8', 4)], 500, False, None, [])]
})

def pin_name(idx):
    return 'Pin {}/{}'.format(idx, ('A' if idx <= 7 else 'B') + str(idx % 8))

def input_channel(idx):
    return {
            'predicate': 'cfg.pinConfiguration{} > 1'.format(idx),
            'id': 'Input {}'.format(idx),
            'label': {'en': 'Input Value {}'.format(idx),
                      'de': 'Eingangswert {}'.format(idx)},

            'type': 'Input Value',

            'getters': [{
                'packet': 'Get Value',
                'element': 'Value',
                'transform': 'value[{}] ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

            'callbacks': [{
                'filter': 'channel == {}'.format(idx),
                'packet': 'Input Value',
                'element': 'Value',
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

            'init_code':"""this.setConfiguration({0}, 'i', cfg.pinConfiguration{0} % 2 == 1);
            this.setInputValueCallbackConfiguration({0}, channelCfg.updateInterval, false);""".format(idx),
            'dispose_code': """this.setInputValueCallbackConfiguration({}, 0, false);""".format(idx),
    }

def output_channel(idx):
    return {
            'predicate': 'cfg.pinConfiguration{} <= 1'.format(idx),
            'id': 'Output {}'.format(idx),
            'label': {'en': 'Output Value {}'.format(idx),
                      'de': 'Ausgabewert {}'.format(idx)},

            'type': 'Output Pin',

            'getters': [{
                'packet': 'Get Value',
                'element': 'Value',
                'transform': 'value[{}] ? OnOffType.ON : OnOffType.OFF'.format(idx)}],

            'setters': [{
                'packet': 'Set Selected Value',
                'element': 'Value',
                'packet_params': [str(idx), 'cmd == OnOffType.ON'],
                'command_type': "OnOffType",
            }],


            'callbacks': [{
                'packet': 'Monoflop Done',
                'element': 'Value',
                'filter': 'channel == {}'.format(idx),
                'transform': 'value ? OnOffType.ON : OnOffType.OFF'}],


            'init_code':"""this.setConfiguration({0}, 'o', cfg.pinConfiguration{0} % 2 == 1);""".format(idx),
    }

def monoflop_channel(idx):
    return {
        'predicate': 'cfg.pinConfiguration{} <= 1'.format(idx),
        'id': 'Monoflop {}'.format(idx),
        'label': {'en': 'Monoflop {}'.format(idx),
                  'de': 'Monoflop {}'.format(idx)},
        'type': 'Monoflop',

        'getters': [{
            'packet': 'Get Monoflop',
            'element': 'Value',
            'packet_params': [str(idx)],
            'transform': 'value.value ? OnOffType.ON : OnOffType.OFF'}],

        'setters': [{
            'packet': 'Set Monoflop',
            'packet_params': [str(idx), 'channelCfg.monoflopValue.booleanValue()', 'channelCfg.monoflopDuration'],
            'command_type': "StringType", # Command type has to be string type to be able to use command options.
        }],

        'setter_refreshs': [{
            'channel': 'Output {}'.format(idx),
            'delay': '0'
        }]
    }


def edge_count_channel(idx):
    return {
            'predicate': 'cfg.pinConfiguration{} > 1'.format(idx),
            'id': 'Edge Count {0}'.format(idx),
            'type': 'Edge Count',
            'label': {'en': 'Edge Count {0}'.format(idx),
                      'de': 'Flankenzähler {0}'.format(idx)},

            'init_code':"""this.setEdgeCountConfiguration({0}, channelCfg.edgeType, channelCfg.debounce);""".format(idx),

            'getters': [{
                'packet': 'Get Edge Count',
                'element': 'Count',
                'packet_params': [str(idx), 'channelCfg.resetOnRead'],
                'transform': 'new {number_type}(value{divisor}{unit})'}],

        }

def pin_config(idx):
    return {
            'virtual': True,
            'packet': 'Set Configuration', # This is set only so that the documentation generator can link to the thing configuration from the get configuration action
            'name': 'Pin Configuration {}'.format(idx),
            'type': 'integer',
            'default': 3,
            'options': [
                ({'en': 'Input with pull-up', 'de': 'Eingang mit Pull-Up'}, 3),
                ({'en': 'Input without pull-up', 'de': 'Eingang ohne Pull-Up'}, 2),
                ({'en': 'Output (Initial high)', 'de': 'Ausgang (initial high)'}, 1),
                ({'en': 'Output (Initial low)', 'de': 'Ausgang (initial low)'}, 0)
            ],
            'limit_to_options': 'true',
            'label': {'en': 'Pin Configuration {}'.format(idx), 'de': 'Pin-Konfiguration {}'},
            'description': {'en': 'Configures pin {} as input or output. Inputs without pull-up will be floating if nothing is connected. Outputs can have an initial state of low or high.'.format(idx),
                            'de': 'Konfiguriert Pin {} as Ein- oder Ausgang. Eingänge ohne Pull-Up sind potentialfrei wenn nicht verbunden. Ausgänge können einen Initialzustand von low oder high haben.'.format(idx)}
        }

channels = [input_channel(i) for i in range(0, 16)] + [output_channel(i) for i in range(0, 16)] + [monoflop_channel(i) for i in range(0, 16)] + [edge_count_channel(i) for i in range(0, 16)]
params = [pin_config(i) for i in range(0, 16)]

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.OnOffType', 'org.eclipse.smarthome.core.library.types.StringType'],
    'params': params,
    'channels': channels,
    'channel_types': [
        oh_generic_channel_type('Input Value', 'Switch', 'NOT USED',
                    update_style='Callback Configuration',
                    description={'en': 'The logic level that is currently measured on the pin.',
                                 'de': 'Der Logikpegel, der aktuell auf dem Pin gemessen wird.'}),
        oh_generic_channel_type('Output Pin', 'Switch', 'NOT USED',
                    update_style=None,
                    description={'en': 'The logic level that is currently set on the pin.',
                                 'de': 'Der Logikpegel, der aktuell auf dem Pin ausgegeben wird.'}),
        {
            'id': 'Monoflop',
            'item_type': 'String',
            'params': [{
                'packet': 'Set Monoflop',
                'element': 'Time',

                'name': 'Monoflop Duration',
                'type': 'integer',
                'default': 1000,
                'unit': 'ms',

                'label': {'en': 'Monoflop Duration', 'de': 'Monoflop-Dauer'},
                'description': {'en': 'The time that the pin should hold the configured value.',
                                'de': 'Die Zeit, für die der Pin den konfigurierten Wert halten soll.'}
            },
            {
                'packet': 'Set Monoflop',
                'element': 'Value',

                'name': 'Monoflop Value',
                'type': 'boolean',
                'default': 'true',

                'label': {'en': 'Monoflop Value', 'de': 'Monoflop-Zustand'},
                'description': {'en': 'The desired value of the pin.',
                                'de': 'Der gewünschte Zustand des Pin. '}
            }],
            'label': 'NOT USED',
            'description': {'en': 'Triggers a monoflop as configured.', 'de': 'Löst einen Monoflop mit den konfigurierten Eigenschaften aus.'},
            'command_options': [('Trigger', 'TRIGGER')]
        },
        oh_generic_channel_type('Edge Count', 'Number', 'NOT USED',
            update_style=None,
            description={'en': 'The current value of the edge counter of the pin.',
                         'de': 'Der aktuelle Wert des Flankenzählers des Pins.'},
            params=[{
                'packet': 'Set Edge Count Configuration',
                'element': 'Edge Type',

                'name': 'Edge Type',
                'type': 'integer',
                'label': {'en': 'Edge Type', 'de': 'Flankentyp'},
                'description': {'en': 'Configures if rising edges, falling edges or both are counted.',
                                'de': 'Konfiguriert den zu zählenden Flankentyp. Es können steigende, fallende oder beide Flanken gezählt werden.'}
            },{
                'packet': 'Set Edge Count Configuration',
                'element': 'Debounce',

                'name': 'Debounce',
                'type': 'integer',
                'label': {'en': 'Debounce Time', 'de': 'Entprellzeit'},
                'description': {'en': 'The debounce time is the minimum time between two count increments.',
                                'de': 'Die Entprellzeit ist die Minimalzeit zwischen zwei Zählererhöhungen.'}
            },{
                'packet': 'Get Edge Count',
                'element': 'Reset Counter',

                'name': 'Reset On Read',
                'type': 'boolean',

                'default': 'false',

                'label': {'en': 'Reset Edge Counter On Update', 'de': 'Flankenzähler bei Update zurücksetzen'},
                'description': {'en': 'Enabling this will reset the edge counter after openHAB reads its value. Use this if you want relative counts per update.',
                                'de': 'Wenn aktiviert, wird der Flankenzähler jedes Mal wenn openHAB dessen Wert liest zurückgesetzt. Dann wird eine relative Zählung pro Update ausgegeben.'}
            }])
    ],
    'actions': [{'fn': 'Set Value', 'refreshs': ['Output {}'.format(i) for i in range(0, 16)] + ['Monoflop {}'.format(i) for i in range(0, 16)]},
                {'fn': 'Set Selected Value', 'refreshs': ['Output {}'.format(i) for i in range(0, 16)] + ['Monoflop {}'.format(i) for i in range(0, 16)]},
                {'fn': 'Set Monoflop', 'refreshs': ['Output {}'.format(i) for i in range(0, 16)] + ['Monoflop {}'.format(i) for i in range(0, 16)]},
                'Get Value', 'Get Configuration',
                {'fn': 'Get Edge Count', 'refreshs': ['Edge Count {}'.format(i) for i in range(0, 16)]},
                'Get Monoflop', 'Get Edge Count Configuration']
}
