"""Constants for ZWaveMe."""
# Base component constants
NAME = "Z-Wave-Me"
DOMAIN = "zwave_me"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ATTRIBUTION = "Z-Wave-Me"
ISSUE_URL = "https://github.com/Z-Wave-Me/ha-core/pulls"

ZWAVEPLATFORMS = [
    "sensorMultilevel",
    "switchMultilevel",
    "sensorBinary",
    "switchBinary",
    "thermostat",
    "doorlock",
    "switchRGBW",
    "switchRGB",
    "toggleButton",
]

PLATFORMS = [
    "sensor",
    "binary_sensor",
    "switch",
    "number",
    "climate",
    "lock",
    "light",
    "button",
]
# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"

ZWAVE_ME_NEW_SENSOR = "zwave_me_new_sensorMultilevel"
ZWAVE_ME_NEW_BINARY_SENSOR = "zwave_me_new_sensorBinary"
ZWAVE_ME_NEW_SWITCH = "zwave_me_new_switchBinary"
ZWAVE_ME_NEW_NUMBER = "zwave_me_new_"
ZWAVE_ME_NEW_CLIMATE = "zwave_me_new_climate"
ZWAVE_ME_NEW_LOCK = "zwave_me_new_lock"
ZWAVE_ME_NEW_LIGHT = "zwave_me_new_light"
ZWAVE_ME_NEW_BUTTON = "zwave_me_new_button"
ZWAVE_ME_UPDATE_DEVICE = "zwave_me_update_device"

# Configuration and options
CONF_ENABLED = "enabled"
CONF_URL = "url"
CONF_TOKEN = "token"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a ZWave-Me!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
