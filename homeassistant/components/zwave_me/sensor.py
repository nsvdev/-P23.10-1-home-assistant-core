"""Representation of a sensorMultilevel."""
import logging

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
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

_LOGGER = logging.getLogger(__name__)
# TODO map configs
SENSORS_MAP: dict[str, SensorEntityDescription] = {
    "meterElectric_watt": SensorEntityDescription(
        key="meterElectric_watt",
        device_class=DEVICE_CLASS_POWER,
        native_unit_of_measurement="W",
        icon="mdi:flash-outline",
    ),
    "meterElectric_kilowatt_hour": SensorEntityDescription(
        key="meterElectric_kilowatt_hour",
        device_class=DEVICE_CLASS_ENERGY,
        native_unit_of_measurement="KW/h",
        icon="mdi:current-ac",
    ),
    "meterElectric_voltage": SensorEntityDescription(
        key="meterElectric_voltage",
        device_class=DEVICE_CLASS_VOLTAGE,
        native_unit_of_measurement="V",
        icon="mdi:power-plug",
    ),
    "light": SensorEntityDescription(
        key="light",
        device_class=DEVICE_CLASS_ILLUMINANCE,
        native_unit_of_measurement="lx",
        icon="mdi:car-parking-lights",
    ),
    "noise": SensorEntityDescription(
        key="noise",
        device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
        native_unit_of_measurement="Db",
        icon="mdi:surround-sound",
    ),
    "currentTemperature": SensorEntityDescription(
        key="currentTemperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
    ),
    "temperature": SensorEntityDescription(
        key="temperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        icon="mdi:thermometer",
    ),
}


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    sensors = []
    myzwave = hass.data[DOMAIN]
    for device in myzwave.get_devices_by_device_type("sensorMultilevel"):
        sensor = ZWaveMeSensor(hass, device)
        sensors.append(sensor)
        hass.data[DOMAIN].entities[sensor.unique_id] = sensor
    hass.data[DOMAIN].adding["sensorMultilevel"] = add_entities
    add_entities(sensors)


class ZWaveMeSensor(ZWaveMeDevice, SensorEntity):
    """Representation of a ZWaveMe sensor."""

    def __init__(self, hass, device, sensor=None):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)
        self._sensor = device.probeType
        self._attributes = {}

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSORS_MAP[self._sensor].native_unit_of_measurement

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.get_device().level

    @property
    def name(self):
        """Return the state of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon."""
        return SENSORS_MAP[self._sensor].icon
