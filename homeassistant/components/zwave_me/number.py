"""Representation of a switchMultilevel."""
import logging
from datetime import timedelta

from homeassistant.components.number import NumberEntity
from homeassistant.const import TEMP_CELSIUS

from .__init__ import ZWaveMeDevice
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    sensors = []
    zwaveme = hass.data[DOMAIN]
    for device in zwaveme.get_devices_by_device_type("switchMultilevel"):
        sensor = ZWaveMeNumber(hass, device)
        sensors.append(sensor)
        hass.data[DOMAIN].entities[sensor.unique_id] = sensor
    hass.data[DOMAIN].adding["switchMultilevel"] = add_entities
    add_entities(sensors)


class ZWaveMeNumber(ZWaveMeDevice, NumberEntity):
    """Representation of a ZWaveMe Multilevel Switch."""

    def __init__(self, hass, device, sensor=None):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)

    @property
    def value(self):
        """Return the unit of measurement."""
        return self.get_device().level

    def set_value(self, value: float) -> None:
        """Update the current value."""
        self._hass.data[DOMAIN].zwave_api.send_command(
            self._deviceid, "exact?level=" + str(round(value))
        )

    @property
    def name(self):
        """Return the state of the sensor."""
        return self._name
