"""Representation of an RGB light."""
import logging

from homeassistant.components.light import COLOR_MODE_RGB, LightEntity, ATTR_RGB_COLOR
from .__init__ import ZWaveMeDevice
from .const import DOMAIN
from homeassistant.helpers.dispatcher import async_dispatcher_connect

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the light platform."""

    def add_new_device(new_device):
        rgb = ZWaveMeRGB(new_device)
        add_entities(
            [
                rgb,
            ]
        )

    async_dispatcher_connect(
        hass, "ZWAVE_ME_NEW_" + "switchRGBW".upper(), add_new_device
    )
    async_dispatcher_connect(
        hass, "ZWAVE_ME_NEW_" + "switchRGB".upper(), add_new_device
    )


class ZWaveMeRGB(ZWaveMeDevice, LightEntity):
    """Representation of a ZWaveMe light."""

    def __init__(self, device):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, device)

    def turn_off(self, **kwargs):
        """Turn the device on."""
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, "off")

    def turn_on(self, **kwargs):
        """Turn the device on."""
        color = kwargs.get(ATTR_RGB_COLOR)
        # brightness = kwargs.get(ATTR_BRIGHTNESS)

        if color is None:
            color = [122, 122, 122]
        cmd = "exact?red={}&green={}&blue={}".format(*color)
        # TODO brightness add
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, cmd)

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.device.level == "on"

    @property
    def brightness(self) -> int:
        """Return the brightness of a device."""
        return max(self.device.color.values())

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        """Return the rgb color value [int, int, int]."""
        rgb = self.device.color
        values = (rgb["r"], rgb["g"], rgb["b"])  # ensure order
        return values

    @property
    def supported_color_modes(self) -> set:
        """Return all color modes."""
        return {COLOR_MODE_RGB}

    @property
    def color_mode(self) -> str:
        """Return current color mode."""
        return COLOR_MODE_RGB

    @property
    def name(self):
        """Return the state of the sensor."""
        return self._name
