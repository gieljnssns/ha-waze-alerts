"""
Custom integration to integrate Ha waze alerts with Home Assistant.

For more details about this integration, please refer to
https://github.com/gieljnssns/ha-waze-alerts
"""

from __future__ import annotations

from typing import TYPE_CHECKING


import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_state_change
from .const import DOMAIN
from .helper import send_location_to_api

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Location Tracker component."""
    _LOGGER.info("Setting up Location Tracker")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a config entry."""
    _LOGGER.info(f"Setting up config entry for {DOMAIN}")

    # Sla configuratie op in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Start monitoring device_tracker
    async def location_changed(entity_id, old_state, new_state):
        if not old_state or not new_state:
            return
        new_lat = new_state.attributes.get("latitude")
        new_lon = new_state.attributes.get("longitude")
        radius = entry.data["radius"]
        categories = entry.data["categories"]

        if new_lat and new_lon:
            _LOGGER.info(f"Device moved to: {new_lat}, {new_lon}")
            # Call helper to send location
            await send_location_to_api(hass, new_lat, new_lon, radius, categories)

    async_track_state_change(
        hass, entry.data["device_tracker"], location_changed
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

# from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
# from homeassistant.helpers.aiohttp_client import async_get_clientsession
# from homeassistant.loader import async_get_loaded_integration

# from .api import IntegrationBlueprintApiClient
# from .coordinator import BlueprintDataUpdateCoordinator
# from .data import IntegrationBlueprintData

# if TYPE_CHECKING:
#     from homeassistant.core import HomeAssistant

#     from .data import IntegrationBlueprintConfigEntry

# PLATFORMS: list[Platform] = [
#     Platform.SENSOR,
#     Platform.BINARY_SENSOR,
#     Platform.SWITCH,
# ]


# # https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
# async def async_setup_entry(
#     hass: HomeAssistant,
#     entry: IntegrationBlueprintConfigEntry,
# ) -> bool:
#     """Set up this integration using UI."""
#     coordinator = BlueprintDataUpdateCoordinator(
#         hass=hass,
#     )
#     entry.runtime_data = IntegrationBlueprintData(
#         client=IntegrationBlueprintApiClient(
#             username=entry.data[CONF_USERNAME],
#             password=entry.data[CONF_PASSWORD],
#             session=async_get_clientsession(hass),
#         ),
#         integration=async_get_loaded_integration(hass, entry.domain),
#         coordinator=coordinator,
#     )

#     # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
#     await coordinator.async_config_entry_first_refresh()

#     await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
#     entry.async_on_unload(entry.add_update_listener(async_reload_entry))

#     return True


# async def async_unload_entry(
#     hass: HomeAssistant,
#     entry: IntegrationBlueprintConfigEntry,
# ) -> bool:
#     """Handle removal of an entry."""
#     return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


# async def async_reload_entry(
#     hass: HomeAssistant,
#     entry: IntegrationBlueprintConfigEntry,
# ) -> None:
#     """Reload config entry."""
#     await async_unload_entry(hass, entry)
#     await async_setup_entry(hass, entry)
