"""Constants for ha-waze-alerts."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "ha_waze_alerts"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
DEFAULT_RADIUS = 1000 #in meters

CATEGORIES = ["ACCIDENT", "JAM", "POLICE", "WEATHERHAZARD", "HAZARD", "CONSTRUCTION", "ROAD_CLOSED"]