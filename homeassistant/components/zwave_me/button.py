"""Representation of a toggleButton."""
import logging
from datetime import timedelta

from homeassistant.components.binary_sensor import DEVICE_CLASS_MOTION
from homeassistant.components.button import ButtonEntity

from .__init__ import ZWaveMeDevice
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


# TODO MAPPING


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the button platform."""
    # We only want this platform to be set up via discovery.
    buttones = []
    for device in hass.data[DOMAIN].get_devices_by_device_type("toggleButton"):
        button = ZWaveMeButton(hass, device)
        buttones.append(button)
        hass.data[DOMAIN].entities[button.unique_id] = button
    hass.data[DOMAIN].adding["toggleButton"] = add_entities

    add_entities(buttones)


class ZWaveMeButton(ZWaveMeDevice, ButtonEntity):
    """Representation of a ZWaveMe button."""

    def __init__(self, hass, device):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)
        self._sensor = device.probeType
        self._attributes = {}

    @property
    def name(self):
        """Return the state of the button."""
        return self._name

    def press(self, **kwargs) -> None:
        """Turn the entity on."""
        self._hass.data[DOMAIN].zwave_api.send_command(self._deviceid, "on")

    @property
    def device_class(self) -> str:
        """Return the device class."""
        # TODO ICONS
        return DEVICE_CLASS_MOTION
