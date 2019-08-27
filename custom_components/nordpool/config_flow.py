"""Adds config flow for nordpool."""
from collections import OrderedDict

import voluptuous as vol
from homeassistant.core import callback
from homeassistant import config_entries

from . import DOMAIN

import logging
_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class NordpoolFlowHandler(config_entries.ConfigFlow):
    """Config flow for Nordpool."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(
        self, user_input=None
    ):  # pylint: disable=dangerous-default-value
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Elspot", data=user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""
        data_schema = OrderedDict()
        data_schema[vol.Required("region", default="Kr.sand")] = str
        data_schema[vol.Optional("friendly_name", default="")] = str
        # This is only needed if you want the some area but want the prices in a non local currency
        data_schema[vol.Optional("currency", default="")] = str
        data_schema[vol.Optional("VAT", default=True)] = bool
        data_schema[vol.Optional("precision", default=3)] = vol.Coerce(int)
        data_schema[vol.Optional("low_price_cutoff", default=1.0)] = vol.Coerce(float)
        data_schema[vol.Optional("price_type", default="kWh")] = str

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=self._errors
        )

    async def async_step_import(self, user_input):  # pylint: disable=unused-argument
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        return self.async_create_entry(title="configuration.yaml", data={})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return NordpoolOptionsHandler(config_entry)


class NordpoolOptionsHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry
        self.options = dict(config_entry.options)
        self._errors = {}

    async def async_step_init(self, user_input=None):
        _LOGGER.info("user input %r" % user_input)

        _LOGGER.info('%r' % dict(self.config_entry.options))
        _LOGGER.info('%r' % dict(self.config_entry.data))
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        old_settings = self.config_entry.data
        # for k, v in self.options.items():
        #     _LOGGER.info('%s %s', k, v)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "region", default=old_settings.get("region", "")
                    ): str,
                    vol.Optional(
                        "friendly_name",
                        default=old_settings.get("friendly_name", ""),
                    ): str,
                    vol.Optional(
                        "currency",
                        default=old_settings.get("currency", ""),
                    ): str,
                    vol.Optional(
                        "VAT", default=old_settings.get("VAT", True)
                    ): bool,
                    vol.Optional(
                        "precision", default=old_settings.get("precision", 3)
                    ): vol.Coerce(int),
                    vol.Optional(
                        "low_price_cutoff",
                        default=self.config_entry.options.get("low_price_cutoff", 1.0),
                    ): vol.Coerce(float),
                    vol.Optional(
                        "price_type",
                        default=old_settings.get("price_type", "kWh"),
                    ): str,
                }
            ),
        )

    async def _show_config_form(self, user_input=None):
        # https://github.com/thomasloven/hass-favicon/blob/master/custom_components/favicon/__init__.py#L25
        #
