"""Representation of a switchBinary."""
import logging
from datetime import timedelta

from .__init__ import ZWaveMeDevice
from .const import DOMAIN
from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOTION,
    BinarySensorEntity, BinarySensorEntityDescription,
)
from homeassistant.helpers.dispatcher import async_dispatcher_connect

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)
# TODO SENSOR MAP
SENSORS_MAP: dict[str, BinarySensorEntityDescription] = {
    "generic": BinarySensorEntityDescription(
        key="motion",
        device_class=DEVICE_CLASS_MOTION,
    ),
    "motion": BinarySensorEntityDescription(
        key="motion",
        device_class=DEVICE_CLASS_MOTION,
    )
}
DEVICE_NAME = "sensorBinary"


async def async_setup_entry(hass, entry, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    def add_new_device(new_device):
        sensor = create_device(new_device)
        add_entities([sensor, ])

    def create_device(new_device):
        if new_device.probeType in SENSORS_MAP:
            description = SENSORS_MAP.get(new_device.probeType)
        else:
            description = SENSORS_MAP['generic']

        sensor = ZWaveMeBinarySensor(new_device, description)
        hass.data[DOMAIN].entities[sensor.unique_id] = sensor
        return sensor

    sensors = []
    for device in hass.data[DOMAIN].get_devices_by_device_type(DEVICE_NAME):
        sensor = create_device(device)
        sensors.append(sensor)
        hass.data[DOMAIN].entities[sensor.unique_id] = sensor
    hass.data[DOMAIN].adding[DEVICE_NAME] = add_entities
    add_entities(sensors)

    async_dispatcher_connect(hass, "ZWAVE_ME_NEW_" + DEVICE_NAME.upper(),
                             add_new_device)


class ZWaveMeBinarySensor(ZWaveMeDevice, BinarySensorEntity):
    """Representation of a ZWaveMe binary sensor."""

    def __init__(self, device, description):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, device)
        self.entity_description = description

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.device.level == "on"

    @property
    def name(self) -> str:
        """Return the state of the sensor."""
        return self._name
