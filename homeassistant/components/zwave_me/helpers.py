from dataclasses import dataclass, field
from typing import Union

FIELDS = ["id", "deviceType", "probeType"]
METRICS_SCALE = ["title", "level", "scaleTitle", "min", "max", "color"]


@dataclass
class ZWaveMeData:
    id: str
    deviceType: str
    title: str
    level: Union[str, int]
    probeType: str = ""
    scaleTitle: str = ""
    min: str = ""
    max: str = ""
    color: dict = field(default_factory=dict)


def prepare_devices(devices):
    prepared_devices = []
    for device in devices:
        prepared_device = {
            **{key: device[key] for key in FIELDS},
            **{
                key: device["metrics"][key]
                for key in METRICS_SCALE
                if key in device["metrics"]
            },
        }
        prepared_devices.append(prepared_device)
    return [ZWaveMeData(**d) for d in prepared_devices]


def create_entity(hass, device: ZWaveMeData):
    from .binary_sensor import ZWaveMeBinarySensor
    from .climate import ZWaveMeClimate
    from .light import ZWaveMeRGB
    from .lock import ZWaveMeLock
    from .number import ZWaveMeNumber
    from .sensor import ZWaveMeSensor
    from .switch import ZWaveMeSwitch
    from .button import ZWaveMeButton

    ENTITIES_MAP = {
        "sensorMultilevel": ZWaveMeSensor,
        "switchMultilevel": ZWaveMeNumber,
        "sensorBinary": ZWaveMeBinarySensor,
        "switchBinary": ZWaveMeSwitch,
        "thermostat": ZWaveMeClimate,
        "doorlock": ZWaveMeLock,
        "switchRGBW": ZWaveMeRGB,
        "switchRGB": ZWaveMeRGB,
        "toggleButton": ZWaveMeButton,
    }
    return ENTITIES_MAP[device.deviceType](hass, device)
