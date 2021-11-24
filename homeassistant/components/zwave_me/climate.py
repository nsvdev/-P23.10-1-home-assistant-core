"""Representation of a thermostat."""
import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    CURRENT_HVAC_HEAT,
    SUPPORT_TARGET_TEMPERATURE,
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
)
from homeassistant.const import ATTR_TEMPERATURE

from .__init__ import ZWaveMeDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
TEMPERATURE_DEFAULT_STEP = 0.5


async def async_setup_entry(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    climates = []
    myzwave = hass.data[DOMAIN]
    for device in myzwave.get_devices_by_device_type("thermostat"):
        climate = ZWaveMeClimate(hass, device)
        climates.append(climate)
        hass.data[DOMAIN].entities[climate.unique_id] = climate
    hass.data[DOMAIN].adding["thermostat"] = add_entities
    add_entities(climates)


class ZWaveMeClimate(ZWaveMeDevice, ClimateEntity):
    """Representation of a ZWaveMe sensor."""

    def __init__(self, hass, device, sensor=None):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)
        self._sensor = device.probeType

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return

        self._hass.data[DOMAIN].zwave_api.send_command(
            self._deviceid, "exact?level=" + str(temperature)
        )

    def set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        pass

    @property
    def temperature_unit(self):
        """Return the temperature_unit."""
        return self.get_device().scaleTitle

    @property
    def target_temperature(self):
        """Return the state of the sensor."""
        return self.get_device().level

    @property
    def max_temp(self):
        """Return the state of the sensor."""
        return self.get_device().max

    @property
    def min_temp(self):
        """Return the state of the sensor."""
        return self.get_device().min

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        modes = [HVAC_MODE_COOL, HVAC_MODE_HEAT]  # placeholder
        # modes = self.get_device()["metrics"]["modes"] # TODO Add modes
        return modes

    @property
    def hvac_action(self) -> str:
        """Return the current action."""
        action = CURRENT_HVAC_HEAT  # placeholder
        # action = self.get_device()["metrics"]["action"] # TODO Add action
        # TODO: or maybe with switchBinary
        # switch = self.get_device()["switch_id"]
        # action = self.hass.data[DOMAIN].get_device(switch)["metrics"]["level"]
        return action

    @property
    def hvac_mode(self) -> str:
        """Return the current mode."""
        mode = HVAC_MODE_HEAT  # placeholder
        # mode = self.get_device()["metrics"]["current_mode"] # TODO Add mode
        return mode

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return TEMPERATURE_DEFAULT_STEP

    @property
    def name(self):
        """Return the state of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:thermometer"
