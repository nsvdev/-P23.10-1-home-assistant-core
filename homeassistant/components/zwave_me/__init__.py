"""The Z-Wave-Me WS integration."""
import logging
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from zwave_ws import ZWaveMe

from .helpers import ZWaveMeData, create_entity, prepare_devices
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
    hass.data[DOMAIN] = ZWaveMeController(hass, entry)
    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


class ZWaveMeController:
    def __init__(self, hass, config):
        self.entities = {}
        self._devices = []
        self.adding = {}
        self._hass = hass
        self._config = config
        self.zwave_api = ZWaveMe(
            on_device_create=self.on_device_create,
            on_device_update=self.on_device_update,
            on_new_device=self.add_device,
            token=self._config.data["token"],
            url=self._config.data["url"],
            platforms=ZWAVEPLATFORMS,
        )

    def add_device(self, device: ZWaveMeData):
        new_device = prepare_devices(
            [
                device,
            ]
        )[0]
        new_entity = create_entity(self._hass, new_device)
        self.entities[new_entity.unique_id] = new_entity
        self._devices.append(new_device)
        self.adding[new_device.deviceType](
            [
                new_entity,
            ]
        )

    def get_devices(self):
        return self._devices

    def get_devices_by_device_type(self, device_type):
        return [device for device in self._devices if device.deviceType == device_type]

    def get_device(self, deviceid):
        for device in self.get_devices():
            if device.id.lower() == deviceid.lower():
                return device

    def on_device_create(self, devices):
        self._devices = prepare_devices(devices)
        self._hass.config_entries.async_setup_platforms(self._config, PLATFORMS)

    def on_device_update(self, dict_data):
        for device in self._devices:
            if device.id == dict_data["id"]:
                if device.deviceType == "sensorMultilevel":
                    device.level = round(float(dict_data["metrics"]["level"]), 1)
                else:
                    device.level = dict_data["metrics"]["level"]
                if "min" in dict_data["metrics"]:
                    device.min = dict_data["metrics"]["min"]
                if "max" in dict_data["metrics"]:
                    device.max = dict_data["metrics"]["max"]
                if "color" in dict_data["metrics"]:
                    device.color = dict_data["metrics"]["color"]

                if DOMAIN + "." + dict_data["id"] in self.entities:
                    self.entities[
                        DOMAIN + "." + dict_data["id"]
                    ].schedule_update_ha_state()
                break


class ZWaveMeDevice(Entity):
    """Representation of a ZWaveMe device."""

    def __init__(self, hass, device):
        """Initialize the device."""
        self._name = device.title
        self._outlet = None
        self._probeType = device.probeType
        self._state = device.level

        self._hass = hass
        self._deviceid = device.id

        self._attributes = {
            "device_id": self._deviceid,
        }

    def get_device(self):
        """Get device info by id."""
        for device in self._hass.data[DOMAIN].get_devices():
            if device.id == self._deviceid:
                return device

        return None

    def get_state(self):
        """Get status of a generic device."""
        # TODO is failed status
        device = self.get_device()
        if "temperature" in device.probeType and device.level != "unavailable":
            self._attributes["temperature"] = device.level

    def get_available(self):
        """Get availability of a generic device."""
        device = self.get_device()
        # return device.availability # TODO is available
        return True

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
