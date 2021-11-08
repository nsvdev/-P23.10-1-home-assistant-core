"""Config flow to configure ZWaveMe integration."""

import logging

import voluptuous as vol
from homeassistant import config_entries

from .const import CONF_URL, CONF_TOKEN, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ZWaveMeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ZWaveMe integration config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self.url = vol.UNDEFINED
        self.token = vol.UNDEFINED

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            self.url = user_input["url"]
            self.token = user_input["token"]

            # Steps for login checking and error handling needed here
            return self.async_create_entry(
                title=user_input[CONF_URL],
                data=user_input,
                description_placeholders={
                    "docs_url": "https://zwayhomeautomation.docs.apiary.io/"
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TOKEN): str,
                    vol.Required(CONF_URL): str,
                }
            ),
            description_placeholders={
                "docs_url": "https://zwayhomeautomation.docs.apiary.io/"
            },
            errors=errors,
        )

    async def async_step_import(self, user_input):
        """Import a config flow from configuration."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        token = user_input[CONF_TOKEN]
        url = user_input[CONF_URL]
        # code for validating login information and error handling needed

        return self.async_create_entry(
            title=f"{url} (from configuration)",
            data={
                CONF_TOKEN: token,
                CONF_URL: url,
            },
        )
