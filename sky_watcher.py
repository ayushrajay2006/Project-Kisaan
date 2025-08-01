# sky_watcher.py
# This agent is responsible for providing weather forecasts.

import logging

def get_weather_forecast(text: str):
    """
    Simulates fetching a weather forecast.

    In a real application, this function would:
    1. Extract a location from the user's text (e.g., "Hyderabad").
    2. Call an external weather API (like OpenWeatherMap) with that location.
    3. Parse the API response and format it for the user.

    For now, we will ignore the text and return a hardcoded forecast.

    Args:
        text (str): The transcribed text from the user (currently unused).

    Returns:
        dict: A dictionary containing the simulated weather forecast.
    """
    logging.info("Sky Watcher agent is providing a simulated weather forecast.")

    # Mock forecast data
    mock_forecast = {
        "location": "Hyderabad, Telangana",
        "temperature": "31°C",
        "condition": "Partly cloudy with a chance of thunderstorms in the afternoon.",
        "humidity": "75%",
        "wind_speed": "15 km/h",
        "alert": "Warning: Potential for heavy rain and strong winds between 3 PM and 6 PM. Take necessary precautions for standing crops."
    }

    return {
        "status": "success",
        "data": mock_forecast
    }