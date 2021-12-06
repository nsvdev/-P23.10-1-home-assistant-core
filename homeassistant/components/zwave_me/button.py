"""Representation of a toggleButton."""
import logging
from datetime import timedelta

from homeassistant.components.button import ButtonEntity
from .__init__ import ZWaveMeDevice
from .const import DOMAIN
from homeassistant.helpers.dispatcher import async_dispatcher_connect

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)

DEVICE_NAME = "toggleButton"


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the button platform."""

    def add_new_device(new_device):
        new_button = ZWaveMeButton(new_device)
        hass.data[DOMAIN].entities[new_button.unique_id] = new_button
        add_entities([new_button, ])

    buttons = []
    for device in hass.data[DOMAIN].get_devices_by_device_type(DEVICE_NAME):
        button = ZWaveMeButton(device)
        buttons.append(button)
        hass.data[DOMAIN].entities[button.unique_id] = button
    hass.data[DOMAIN].adding[DEVICE_NAME] = add_entities

    add_entities(buttons)
    async_dispatcher_connect(hass, "ZWAVE_ME_NEW_" + DEVICE_NAME.upper(),
                             add_new_device)


class ZWaveMeButton(ZWaveMeDevice, ButtonEntity):
    """Representation of a ZWaveMe button."""

    def __init__(self, device):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, device)

    @property
    def name(self):
        """Return the state of the button."""
        return self._name

    def press(self, **kwargs) -> None:
        """Turn the entity on."""
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, "on")
