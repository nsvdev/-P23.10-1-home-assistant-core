"""Representation of a RGB Light."""
import logging

from homeassistant.components.light import (
    COLOR_MODE_RGB,
    LightEntity,
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR
)

from .__init__ import ZWaveMeDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the light platform."""
    # We only want this platform to be set up via discovery.
    rgbs = []
    myzwave = hass.data[DOMAIN]
    for device in myzwave.get_devices_by_device_type("switchRGBW") + \
                  myzwave.get_devices_by_device_type("switchRGB"):
        rgb = ZWaveMeRGB(hass, device)
        rgbs.append(rgb)
        hass.data[DOMAIN].entities[rgb.unique_id] = rgb
    add_entities(rgbs)


class ZWaveMeRGB(ZWaveMeDevice, LightEntity):
    """Representation of a ZWaveMe light."""

    def __init__(self, hass, device, sensor=None):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)

    def turn_off(self, **kwargs):
        """Turn the device on."""
        self._hass.data[DOMAIN].send_command(self._deviceid, "off")

    def turn_on(self, **kwargs):
        """Turn the device on."""
        cmd = "exact?red={}&green={}&blue={}".format(*kwargs.get(ATTR_RGB_COLOR))
        #TODO brightness add
        self._hass.data[DOMAIN].send_command(self._deviceid, cmd)

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.get_device()["metrics"]["level"] == "on"

    @property
    def brightness(self) -> int:
        """Return brightness of a device"""
        return max(self.get_device()["metrics"]["color"].values())

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        """Return the rgb color value [int, int, int]."""
        rgb = self.get_device()["metrics"]["color"]
        values = (rgb['r'], rgb['g'], rgb['b'])  # ensure order
        return values

    @property
    def supported_color_modes(self) -> set:
        """Return all color modes."""
        return {COLOR_MODE_RGB}
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True  # self.get_device()['availability'] TODO available

    @property
    def color_mode(self) -> str:
        """Return current color mode."""
        return COLOR_MODE_RGB

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
