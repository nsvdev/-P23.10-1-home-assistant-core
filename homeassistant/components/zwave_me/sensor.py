"""Representation of a sensorMultilevel."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS

from .__init__ import ZWaveMeDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
# TODO map configs
SENSORS_MAP = {
    "power": {"eid": "power", "uom": "W", "icon": "mdi:flash-outline"},
    "current": {"eid": "current", "uom": "A", "icon": "mdi:current-ac"},
    "voltage": {"eid": "voltage", "uom": "V", "icon": "mdi:power-plug"},
    "dusty": {"eid": "dusty", "uom": "µg/m3", "icon": "mdi:select-inverse"},
    "light": {"eid": "light", "uom": "lx", "icon": "mdi:car-parking-lights"},
    "noise": {"eid": "noise", "uom": "Db", "icon": "mdi:surround-sound"},
    "humidity": {"eid": "humidity", "uom": "%", "icon": "mdi:water-percent"},
    "currentTemperature": {
        "eid": "temperature",
        "uom": TEMP_CELSIUS,
        "icon": "mdi:thermometer",
    },
    "temperature": {
        "eid": "temperature",
        "uom": TEMP_CELSIUS,
        "icon": "mdi:thermometer",
    },
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
    add_entities(sensors)


class ZWaveMeSensor(ZWaveMeDevice, SensorEntity):
    """Representation of a ZWaveMe sensor."""

    def __init__(self, hass, device, sensor=None):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)
        self._sensor = device["probeType"]
        self._attributes = {}

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSORS_MAP[self._sensor]["uom"]

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.get_device()["metrics"]["level"]

    @property
    def name(self):
        """Return the state of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon."""
        return SENSORS_MAP[self._sensor]["icon"]
