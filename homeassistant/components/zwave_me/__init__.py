"""The Z-Wave-Me WS integration."""
import logging

import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from zwave_ws import ZWaveMe

from .const import CONF_TOKEN, CONF_URL, DOMAIN, PLATFORMS, ZWAVEPLATFORMS

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {vol.Required(CONF_TOKEN): cv.string, vol.Required(CONF_URL): cv.string},
            extra=vol.ALLOW_EXTRA,
        ),
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup_entry(hass, entry):
    """Set up Z-Wave-Me from a config entry."""
    _LOGGER.debug("Create the main object")
    hass.data[DOMAIN] = ZWaveMe(
        hass,
        entry,
        domain=DOMAIN,
        logger=_LOGGER,
        platforms=PLATFORMS,
        zwaveplatforms=ZWAVEPLATFORMS,
    )
    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


class ZWaveMeDevice(Entity):
    """Representation of a ZWaveMe device."""

    def __init__(self, hass, device):
        """Initialize the device."""
        self._name = device["metrics"]["title"]
        self._outlet = None
        self._probeType = device["probeType"]
        self._state = device["metrics"]["level"]

        self._hass = hass
        self._deviceid = device["id"]

        self._attributes = {
            "device_id": self._deviceid,
        }

    def get_device(self):
        """Get device info by id."""
        for device in self._hass.data[DOMAIN].get_devices():
            if "id" in device and device["id"] == self._deviceid:
                return device

        return None

    def get_state(self):
        """Get status of a generic device."""
        # TODO is failed status
        device = self.get_device()
        if (
            "temperature" in device["probeType"]
            and device["metrics"]["level"] != "unavailable"
        ):
            self._attributes["temperature"] = device["metrics"]["level"]

    def get_available(self):
        """Get availability of a generic device."""
        device = self.get_device()
        return device["visibility"]

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def available(self):
        """Return true if device is online."""
        return self.get_available()

    def update(self):
        """Update device state."""
        pass

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return self._attributes

    @property
    def unique_id(self) -> str:
        """If the switch is currently on or off."""
        # TODO unique id integration
        return DOMAIN + "." + self._deviceid
