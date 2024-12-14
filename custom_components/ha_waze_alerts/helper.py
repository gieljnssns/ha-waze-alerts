import aiohttp
import logging
_LOGGER = logging.getLogger(__name__)
async def send_location_to_api(hass, lat, lon, radius, categories):
    """Send location to external API."""
    url = "https://example.com/api"
    payload = {
        "latitude": lat,
        "longitude": lon,
        "radius": radius,
        "categories": categories,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                _LOGGER.info(f"API response: {data}")
                # Verwerk en haal coördinaten uit de relevante categorieën
                coordinates = [
                    (item["latitude"], item["longitude"])
                    for item in data.get("results", [])
                    if item["category"] in categories
                ]
                _LOGGER.info(f"Relevant coordinates: {coordinates}")
                # Opslaan of doorgeven aan een entiteit
            else:
                _LOGGER.error(f"API error: {response.status}")
