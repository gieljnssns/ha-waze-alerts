"""Adds config flow for Blueprint."""

# from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_MONITORED_CONDITIONS, CONF_RADIUS
from homeassistant.core import callback

from .const import CATEGORIES, DEFAULT_RADIUS, DOMAIN


class WazeAlertsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Location Tracker."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Location Tracker", data=user_input)

        # Haal beschikbare device_trackers op
        device_trackers = list(self.hass.states.async_entity_ids("device_tracker"))

        # Stel het formulier samen
        schema = vol.Schema(
            {
                vol.Required("device_tracker"): vol.In(device_trackers),
                vol.Required(CONF_RADIUS): vol.Coerce(int),
                vol.Required(CONF_MONITORED_CONDITIONS): vol.All(
                    [vol.In(CATEGORIES)], vol.Length(min=1)
                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Define the options flow for updates."""
        return WazeAlertsOptionsFlowHandler(config_entry)


class WazeAlertsOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for Location Tracker."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Required(
                CONF_RADIUS, default=self.config_entry.options.get(CONF_RADIUS, 1000)
            ): vol.Coerce(int),
            vol.Required(
                CONF_MONITORED_CONDITIONS,
                default=self.config_entry.options.get(CONF_MONITORED_CONDITIONS, []),
            ): vol.All([vol.In(CATEGORIES)], vol.Length(min=1)),
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))
