"""Representation of a sensorMultilevel."""
import logging

from homeassistant.components.light import COLOR_MODE_RGB, LightEntity, ATTR_RGB_COLOR

from .__init__ import ZWaveMeDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    rgbs = []
    myzwave = hass.data[DOMAIN]
    for device in myzwave.get_devices_by_device_type(
        "switchRGBW"
    ) + myzwave.get_devices_by_device_type("switchRGB"):
        rgb = ZWaveMeRGB(hass, device)
        rgbs.append(rgb)
        hass.data[DOMAIN].entities[rgb.unique_id] = rgb
    hass.data[DOMAIN].adding["switchRGB"] = add_entities
    hass.data[DOMAIN].adding["switchRGBW"] = add_entities

    add_entities(rgbs)


class ZWaveMeRGB(ZWaveMeDevice, LightEntity):
    """Representation of a ZWaveMe sensor."""

    def __init__(self, hass, device, sensor=None):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)

    def turn_off(self, **kwargs):
        """Turn the device on."""
        self._hass.data[DOMAIN].zwave_api.send_command(self._deviceid, "off")

    def turn_on(self, **kwargs):
        """Turn the device on."""
        color = kwargs.get(ATTR_RGB_COLOR)
        if color is None:
            color = [122, 122, 122]
        cmd = "exact?red={}&green={}&blue={}".format(*color)
        # TODO brightness add
        self._hass.data[DOMAIN].zwave_api.send_command(self._deviceid, cmd)

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.get_device().level == "on"

    @property
    def brightness(self) -> int:
        return max(self.get_device().color.values())

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        """Return the rgb color value [int, int, int]."""
        rgb = self.get_device().color
        values = (rgb["r"], rgb["g"], rgb["b"])  # ensure order
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
        """Return the state of the sensor."""
        return self._name
