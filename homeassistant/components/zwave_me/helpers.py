from zwave_me_ws import ZWaveMeData

import logging

_LOGGER = logging.getLogger(__name__)


def create_entity(hass, device: ZWaveMeData):
    from .binary_sensor import ZWaveMeBinarySensor
    from .binary_sensor import SENSORS_MAP as BINARY_SENSOR_MAP
    from .climate import ZWaveMeClimate
    from .light import ZWaveMeRGB
    from .lock import ZWaveMeLock
    from .number import ZWaveMeNumber
    from .sensor import ZWaveMeSensor
    from .sensor import SENSORS_MAP as MULTILEVEL_MAP
    from .switch import ZWaveMeSwitch
    #from .button import ZWaveMeButton
    ENTITIES_MAP = {
        "sensorMultilevel": ZWaveMeSensor,
        "switchMultilevel": ZWaveMeNumber,
        "sensorBinary": ZWaveMeBinarySensor,
        "switchBinary": ZWaveMeSwitch,
        "thermostat": ZWaveMeClimate,
        "doorlock": ZWaveMeLock,
        "switchRGBW": ZWaveMeRGB,
        "switchRGB": ZWaveMeRGB,
        #"toggleButton": ZWaveMeButton,
    }
    description = None
    if device.deviceType == 'sensorMultilevel':
        description = MULTILEVEL_MAP.get(
            device.probeType if device.probeType in MULTILEVEL_MAP else 'generic')
    elif device.deviceType == 'sensorBinary':
        description = BINARY_SENSOR_MAP.get(
            device.probeType if device.probeType in BINARY_SENSOR_MAP else 'generic')
    if description is not None:
        return ENTITIES_MAP[device.deviceType](hass, device, description)
    else:
        return ENTITIES_MAP[device.deviceType](hass, device)