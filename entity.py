"""Recteq entity helper."""

import logging

from .device import RecteqDevice

from homeassistant.const import TEMP_CELSIUS, TEMP_FAHRENHEIT
from homeassistant.core import callback
from homeassistant.helpers import entity

_LOGGER = logging.getLogger(__name__)

class RecteqEntity(entity.Entity):
    def __init__(
        self,
        device: RecteqDevice,
        dps: str,
        name: str,
        unit: str,
        value,
        device_class: str,
        default_enabled: bool
    ) -> None:
        self._device          = device
        self._dps             = dps
        self._name            = f"{device.name} {name}"
        self._unit            = unit
        self._value           = value
        self._device_class    = device_class
        self._default_enabled = default_enabled

    @property
    def name(self):
        return self._name

    @property
    def entity_registry_enabled_default(self) -> bool:
        return self._default_enabled

    @property
    def attribute_value(self):
        value = self._device.status(self._dps)

        if value is None:
            return None

        return self._value(value)

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def device_class(self):
        return self._device_class

    @property
    def available(self):
        return self._device.available

    @property
    def should_poll(self):
        return False

    async def async_added_to_hass(self):
        self.async_on_remove(self._device.async_add_listener(self._update_callback))

    async def async_update(self):
        await self._device.async_request_refresh()

    @callback
    def _update_callback(self):
        self.async_write_ha_state()

