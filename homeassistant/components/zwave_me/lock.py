"""Representation of a doorlock."""
import logging
from datetime import timedelta

from .__init__ import ZWaveMeDevice
from .const import DOMAIN
from homeassistant.components.lock import LockEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)
DEVICE_NAME = "doorlock"


async def async_setup_entry(hass, entry, add_entities, discovery_info=None):
    """Set up the lock platform."""

    def add_new_device(new_device):
        lock = ZWaveMeLock(new_device)
        add_entities(
            [
                lock,
            ]
        )

    async_dispatcher_connect(
        hass, "ZWAVE_ME_NEW_" + DEVICE_NAME.upper(), add_new_device
    )


class ZWaveMeLock(ZWaveMeDevice, LockEntity):
    """Representation of a ZWaveMe binary sensor."""

    def __init__(self, device):
        """Initialize the device."""
        ZWaveMeDevice.__init__(self, device)

    @property
    def is_locked(self):
        """Return the state of the lock."""
        return self.get_device().level == "close"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    def unlock(self, **kwargs):
        """Send command to unlock the lock."""
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, "open")

    def lock(self, **kwargs):
        """Send command to unlock the lock."""
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, "close")
