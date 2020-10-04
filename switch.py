"""Recteq Switch Component."""
import logging

import json
import pytuya

import voluptuous as vol

from homeassistant.components.switch import (
    SwitchEntity,
    PLATFORM_SCHEMA
)

from homeassistant.const import (
    CONF_NAME,
    CONF_HOST
)

import homeassistant.helpers.config_validation as cv

from time import time
from threading import Lock

from .const import __version__

CONF_DEVICE_ID = 'device_id'
CONF_LOCAL_KEY = 'local_key'
CONF_PROTOCOL = 'protocol'

DPS_POWER  = '1'
DPS_TARGET = '102'
DPS_ACTUAL = '103'
DPS_PROBEA = '105'
DPS_PROBEB = '106'
DPS_ERROR1 = '109'
DPS_ERROR2 = '110'
DPS_ERROR3 = '111'

ATTR_POWER  = 'power'
ATTR_TARGET = 'target'
ATTR_ACTUAL = 'actual'
ATTR_PROBEA = 'probea'
ATTR_PROBEB = 'probeb'
ATTR_ERROR1 = 'error1'
ATTR_ERROR2 = 'error2'
ATTR_ERROR3 = 'error3'

DPS_ATTRS = {
    DPS_POWER:  ATTR_POWER,
    DPS_TARGET: ATTR_TARGET,
    DPS_ACTUAL: ATTR_ACTUAL,
    DPS_PROBEA: ATTR_PROBEA,
    DPS_PROBEB: ATTR_PROBEB,
    DPS_ERROR1: ATTR_ERROR1,
    DPS_ERROR2: ATTR_ERROR2,
    DPS_ERROR3: ATTR_ERROR3,
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_DEVICE_ID): cv.string,
    vol.Required(CONF_LOCAL_KEY): cv.string,
    vol.Optional(CONF_PROTOCOL, default='3.3'): cv.string,
})

log = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    log.info('Setting up %s version %s', __name__, __version__)

    switches = []

    device = RecteqDevice(
        pytuya.OutletDevice(
            config.get(CONF_DEVICE_ID),
            config.get(CONF_HOST),
            config.get(CONF_LOCAL_KEY)
        ),
        config.get(CONF_PROTOCOL)
    )

    switches.append(
        Recteq(
            device,
            config.get(CONF_NAME),
        )
    )

    add_devices(switches)

class RecteqDevice:
    """Wrapper for the Tuya device to cache the status."""

    def __init__(self, device, protocol):
        self._cached_status = ''
        self._cached_status_time = 0
        self._device = device
        self._device.set_version(float(protocol))
        self._lock = Lock()

    def __get_status(self):
        for i in range(3):
            try:
                status = self._device.status()
                log.debug('Status is ' + json.dumps(status))
                return status
            except ConnectionError:
                if i+1 == 3:
                    raise ConnectionError("Failed to update status.")

    def set_status(self, state, switchid):
        self._cached_status = ''
        self._cached_status_time = 0
        return self._device.set_status(state, switchid)

    def status(self):
        self._lock.acquire()
        try:
            now = time()
            if not self._cached_status or now - self._cached_status_time > 20:
                self._cached_status = self.__get_status()
                self._cached_status_time = time()
            return self._cached_status
        finally:
            self._lock.release()

class Recteq(SwitchEntity):
    """The Recteq switch to turn the unit on and off and read attributes."""

    def __init__(self, device, name):
        self._device = device
        self._name = name
        self._state = None
        self._status = self._device.status()

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def device_state_attributes(self):
        attrs = {}
        try:
            for dps, attr in DPS_ATTRS.items():
                attrs[attr] = "{}".format(self._status['dps'][dps])
        except KeyError:
            pass
        return attrs

    def turn_on(self, **kwargs):
        self._device.set_status(True, DPS_POWER)

    def turn_off(self, **kwargs):
        self._device.set_status(False, DPS_POWER)

    def update(self):
        self._status= self._device.status()
        self._state = self._status['dps'][DPS_POWER]

# vim: set et sw=4 ts=4 :
