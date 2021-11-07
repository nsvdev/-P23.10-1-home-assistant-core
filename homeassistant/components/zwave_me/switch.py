"""Representation of a switchBinary."""
import logging
from datetime import timedelta

from homeassistant.components.binary_sensor import DEVICE_CLASS_MOTION
from homeassistant.components.switch import SwitchEntity

from .__init__ import ZWaveMeDevice
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


# TODO MAPPING


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the switch platform."""
    # We only want this platform to be set up via discovery.
    switches = []
    for device in hass.data[DOMAIN].get_devices_by_device_type("switchBinary"):
        switch = ZWaveMeSwitch(hass, device)
        switches.append(switch)
        hass.data[DOMAIN].entities[switch.unique_id] = switch
    add_entities(switches)


class ZWaveMeSwitch(ZWaveMeDevice, SwitchEntity):
    """Representation of a ZWaveMe binary switch."""

    def __init__(self, hass, device):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)
        self._sensor = device["probeType"]
        self._attributes = {}

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self.get_device()["metrics"]["level"] == "on"

    @property
    def name(self):
        """Return the state of the switch."""
        return self._name

    def async_turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        self._hass.data[DOMAIN].send_command(self._deviceid, "on")

    def async_turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        self._hass.data[DOMAIN].send_command(self._deviceid, "off")

    @property
    def device_class(self) -> str:
        """Return the device class."""
        # TODO ICONS
        return DEVICE_CLASS_MOTION
