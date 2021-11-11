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
    add_entities(locks)


class ZWaveMeLock(ZWaveMeDevice, LockEntity):
    """Representation of a ZWaveMe lock."""

    def __init__(self, hass, device):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, hass, device)
        self._attributes = {}

    @property
    def is_locked(self):
        """Return the state of the lock."""
        return self.get_device()["metrics"]["level"] == "close"

    @property
    def name(self):
        """Return the name of the lock."""
        return self._name

    def unlock(self, **kwargs):
        """Unlock the lock"""
        self._hass.data[DOMAIN].send_command(self._deviceid, "open")

    def lock(self, **kwargs):
        """Lock the lock"""
        self._hass.data[DOMAIN].send_command(self._deviceid, "close")
