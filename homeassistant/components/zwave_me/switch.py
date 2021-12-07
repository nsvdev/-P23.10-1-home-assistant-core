"""Representation of a switchBinary."""
import logging
from datetime import timedelta

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_LIGHT,
)
from homeassistant.components.switch import SwitchEntity

from .__init__ import ZWaveMeDevice
from .const import DOMAIN
from homeassistant.helpers.dispatcher import async_dispatcher_connect

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)
DEVICE_NAME = "switchBinary"


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the switch platform."""

    def add_new_device(new_device):
        switch = ZWaveMeSwitch(new_device)
        add_entities(
            [
                switch,
            ]
        )

    async_dispatcher_connect(
        hass, "ZWAVE_ME_NEW_" + DEVICE_NAME.upper(), add_new_device
    )


class ZWaveMeSwitch(ZWaveMeDevice, SwitchEntity):
    """Representation of a ZWaveMe binary switch."""

    def __init__(self, device):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, device)

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self.device.level == "on"

    @property
    def name(self):
        """Return the state of the switch."""
        return self._name

    def turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, "on")

    def turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, "off")

    @property
    def device_class(self) -> str:
        """Return the device class."""
        return DEVICE_CLASS_LIGHT
