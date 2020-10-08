"""The Recteq sensor component."""

import logging

from .const import (
    DOMAIN,
    DPS_TARGET,
    DPS_ACTUAL,
    DPS_PROBEA,
    DPS_PROBEB,
    NAME_TARGET,
    NAME_ACTUAL,
    NAME_PROBEA,
    NAME_PROBEB
)
from .entity import RecteqEntity

from homeassistant.components import sensor
from homeassistant.const import TEMP_FAHRENHEIT

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, add):
    device = hass.data[DOMAIN][entry.entry_id]
    add(
        [
            RecteqTemperatureSensor(device, DPS_TARGET, NAME_TARGET, True),
            RecteqTemperatureSensor(device, DPS_ACTUAL, NAME_ACTUAL, True),
            RecteqTemperatureSensor(device, DPS_PROBEA, NAME_PROBEA, True),
            RecteqTemperatureSensor(device, DPS_PROBEB, NAME_PROBEB, True)
        ]
    )

class RecteqSensor(RecteqEntity):

    @property
    def state(self):
        return self.attribute_value

class RecteqTemperatureSensor(RecteqSensor):

    def __init__(self, device, dps, name, default_enabled):
        super().__init__(
            device,
            dps,
            name,
            TEMP_FAHRENHEIT,
            lambda value: round(value,1),
            sensor.DEVICE_CLASS_TEMPERATURE,
            default_enabled
        )

