"""Constants for the Recteq integration."""

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import homeassistant.const as hac

PROJECT = "Recteq Custom Integration"

VERSION_TUPLE = (0, 0, 0)
VERSION = __version__ = '%d.%d.%d' % VERSION_TUPLE

__author__ = 'Paul Dugas <paul@dugas.cc>'

ISSUE_LINK = 'https://github.com/pdugas/homeassistant-recteq/issues'

DOMAIN = 'recteq'

#PLATFORMS = ["switch", "sensor", "binary_sensor"]
PLATFORMS = ["sensor"]

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
ATTR_PROBEA = 'probe_a'
ATTR_PROBEB = 'probe_b'
ATTR_ERROR1 = 'error_1'
ATTR_ERROR2 = 'error_2'
ATTR_ERROR3 = 'error_3'

NAME_POWER  = 'Power'
NAME_TARGET = 'Target Temperature'
NAME_ACTUAL = 'Actual Temperature'
NAME_PROBEA = 'Probe A Temperature'
NAME_PROBEB = 'Probe B Temperature'
NAME_ERROR1 = 'Error E1'
NAME_ERROR2 = 'Error E2'
NAME_ERROR3 = 'Error E3'

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

DPS_NAMES = {
    DPS_POWER:  NAME_POWER,
    DPS_TARGET: NAME_TARGET,
    DPS_ACTUAL: NAME_ACTUAL,
    DPS_PROBEA: NAME_PROBEA,
    DPS_PROBEB: NAME_PROBEB,
    DPS_ERROR1: NAME_ERROR1,
    DPS_ERROR2: NAME_ERROR2,
    DPS_ERROR3: NAME_ERROR3,
}

PROTOCOL_3_1 = "3.1"
PROTOCOL_3_3 = "3.3"

PROTOCOLS = [PROTOCOL_3_1, PROTOCOL_3_3]

LEN_DEVICE_ID = 20
LEN_LOCAL_KEY = 16

CONF_NAME       = hac.CONF_NAME
CONF_IP_ADDRESS = hac.CONF_IP_ADDRESS
CONF_DEVICE_ID  = 'device_id'
CONF_LOCAL_KEY  = 'local_key'
CONF_PROTOCOL   = 'protocol'

DEFAULT_PROTOCOL = PROTOCOL_3_3

STR_INVALID_PREFIX = "invalid_"
STR_PLEASE_CORRECT = "please_correct"
