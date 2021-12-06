"""Representation of a sensorMultilevel."""
import logging

from homeassistant.components.sensor import SensorEntity, \
    SensorEntityDescription
from homeassistant.const import (
    TEMP_CELSIUS,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TEMPERATURE,
)

from .__init__ import ZWaveMeDevice
from .const import DOMAIN
from homeassistant.helpers.dispatcher import async_dispatcher_connect

_LOGGER = logging.getLogger(__name__)
# TODO map configs
SENSORS_MAP: dict[str, SensorEntityDescription] = {
    "meterElectric_watt": SensorEntityDescription(
        key="meterElectric_watt",
        device_class=DEVICE_CLASS_POWER,
        native_unit_of_measurement="W",
    ),
    "meterElectric_kilowatt_hour": SensorEntityDescription(
        key="meterElectric_kilowatt_hour",
        device_class=DEVICE_CLASS_ENERGY,
        native_unit_of_measurement="KW/h",
    ),
    "meterElectric_voltage": SensorEntityDescription(
        key="meterElectric_voltage",
        device_class=DEVICE_CLASS_VOLTAGE,
        native_unit_of_measurement="V",
    ),
    "light": SensorEntityDescription(
        key="light",
        device_class=DEVICE_CLASS_ILLUMINANCE,
        native_unit_of_measurement="lx",
    ),
    "noise": SensorEntityDescription(
        key="noise",
        device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
        native_unit_of_measurement="Db",
    ),
    "currentTemperature": SensorEntityDescription(
        key="currentTemperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
    "temperature": SensorEntityDescription(
        key="temperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
    "generic": SensorEntityDescription(
        key="temperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
    )
}
DEVICE_NAME = "sensorMultilevel"


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    def add_new_device(new_device):
        sensor = create_device(new_device)
        add_entities([sensor, ])

    def create_device(new_device):
        if new_device.probeType in SENSORS_MAP:
            description = SENSORS_MAP.get(new_device.probeType)
        else:
            description = SENSORS_MAP['generic']

        sensor = ZWaveMeSensor(new_device, description)
        hass.data[DOMAIN].entities[sensor.unique_id] = sensor
        return sensor

    sensors = []
    myzwave = hass.data[DOMAIN]

    for device in myzwave.get_devices_by_device_type(DEVICE_NAME):
        sensor = create_device(device)
        sensors.append(sensor)
        hass.data[DOMAIN].entities[sensor.unique_id] = sensor
    hass.data[DOMAIN].adding[DEVICE_NAME] = add_entities
    add_entities(sensors)
    async_dispatcher_connect(hass, "ZWAVE_ME_NEW_" + DEVICE_NAME.upper(),
                             add_new_device)


class ZWaveMeSensor(ZWaveMeDevice, SensorEntity):
    """Representation of a ZWaveMe sensor."""

    def __init__(self, device, description):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, device)
        self.entity_description = description

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.device.level

    @property
    def name(self):
        """Return the state of the sensor."""
        return self._name
