"""Constants for ha-waze-alerts."""

from logging import Logger, getLogger

import voluptuous as vol

LOGGER: Logger = getLogger(__package__)

DOMAIN = "ha_waze_alerts"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
DEFAULT_RADIUS = 1000  # in meters

CATEGORIES = [
    "ACCIDENT",
    "JAM",
    "POLICE",
    "WEATHERHAZARD",
    "HAZARD",
    "CONSTRUCTION",
    "ROAD_CLOSED",
]

categories_schema = vol.All(
    [vol.In(CATEGORIES)],  # Valideer dat elk item in de lijst een geldige categorie is
    vol.Length(min=1),  # Vereist minimaal 1 selectie
)
