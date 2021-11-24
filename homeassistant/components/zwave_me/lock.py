"""Representation of a lock."""
import logging
from datetime import timedelta

from .__init__ import ZWaveMeDevice
from .const import DOMAIN
from homeassistant.components.lock import LockEntity

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, add_entities, discovery_info=None):
    """Set up the lock platform."""
    locks = []
    for device in hass.data[DOMAIN].get_devices_by_device_type("doorlock"):
        lock = ZWaveMeLock(hass, device)
        locks.append(lock)
        hass.data[DOMAIN].entities[lock.unique_id] = lock
    hass.data[DOMAIN].adding["doorlock"] = add_entities
    add_entities(locks)


class ZWaveMeLock(ZWaveMeDevice, LockEntity):
    """Representation of a ZWaveMe binary sensor."""

    def __init__(self, hass, device):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)
        self._attributes = {}

    @property
    def is_locked(self):
        """Return the state of the lock."""
        return self.get_device().level == "close"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    def unlock(self, **kwargs):
        self._hass.data[DOMAIN].zwave_api.send_command(self._deviceid, "open")

    def lock(self, **kwargs):
        self._hass.data[DOMAIN].zwave_api.send_command(self._deviceid, "close")
