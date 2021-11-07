"""Representation of a switchBinary."""
import logging
from datetime import timedelta

from .__init__ import ZWaveMeDevice
from .const import DOMAIN
from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOTION,
    BinarySensorEntity,
)

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    sensors = []
    for device in hass.data[DOMAIN].get_devices_by_device_type("sensorBinary"):
        sensor = ZWaveMeBinarySensor(hass, device)
        sensors.append(sensor)
        hass.data[DOMAIN].entities[sensor.unique_id] = sensor
    add_entities(sensors)


class ZWaveMeBinarySensor(ZWaveMeDevice, BinarySensorEntity):
    """Representation of a ZWaveMe binary sensor."""

    def __init__(self, hass, device):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)
        self._sensor = device["probeType"]
        self._attributes = {}

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self.get_device()["metrics"]["level"] == "on"

    @property
    def name(self):
        """Return the state of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon."""
        # reference https://icon-sets.iconify.design/mdi/motion-sensor/
        return "mdi:motion-sensor"

    @property
    def device_class(self) -> str:
        """Return the class of the device."""
        # TODO ICONS
        return DEVICE_CLASS_MOTION
