"""The Recteq integration."""

import logging
import pytuya
import async_timeout

from datetime import timedelta
from time import time
from threading import Lock

from .const import DOMAIN, CONF_NAME, DPS_ATTRS

from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.helpers import update_coordinator

MAX_RETRIES = 3
CACHE_SECONDS = 20
UPDATE_INTERVAL = 30

_LOGGER = logging.getLogger(__name__)

class TuyaOutletDeviceWrapper:
    """Wrap pytuya.OutletDevice to cache status lock around polls."""

    def __init__(self, device_id, ip_address, local_key, protocol):
        self._device_id  = device_id
        self._ip_address = ip_address
        self._local_key  = local_key
        self._protocol   = protocol
        self._device = pytuya.OutletDevice(device_id, ip_address, local_key)
        self._device.set_version(float(protocol))
        self._cached_status = None
        self._cached_status_time = None
        self._lock = Lock()
        self.update()

    @property
    def available(self):
        return self._cached_status != None

    def set_status(self, dps, value):
        self._cached_status = None
        self._cached_status_time = None
        return self._device.set_status(value, dps)

    def get_status(self, dps):
        if self._cached_status == None:
            return None
        return self._cached_status[dps]

    def update(self):
        self._lock.acquire()
        try:
            now = time()
            if not self._cached_status or now - self._cached_status_time > CACHE_SECONDS:
                retries = MAX_RETRIES
                while retries:
                    retries -= 1
                    try:
                        self._cached_status = self._device.status()['dps']
                        self._cached_status_time = time()
                        return
                    except ConnectionError as err:
                        if retries <= 0:
                            self._cached_status = None
                            self._cached_status_time = time()
                            raise err
        finally:
            self._lock.release()

    async def async_update(self):
        # FIX ME - this isn't really async!
        self.update()

class RecteqDevice(update_coordinator.DataUpdateCoordinator):

    def __init__(self, hass, entry, outlet: TuyaOutletDeviceWrapper):
        super().__init__(hass, _LOGGER,
            name = entry.data[CONF_NAME],
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        #self._name   = entry.data[CONF_NAME]
        #self._entry  = entry
        self._outlet = outlet

    @property
    def available(self):
        return self._outlet.available

    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(5):
                await self._outlet.async_update()
        except ConnectionError as err:
            raise update_coordinator.UpdateFailed("Error fetching data") from err

    def status(self, dps):
        return self._outlet.get_status(dps)

    @property
    def device_state_attributes(self):
        return {
            attr: self.status(dps)
            for dps, attr in DPS_ATTRS.items()
        }
