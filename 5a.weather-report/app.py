import os
from autogen import ConversableAgent
from autogen import register_function

from typing import Annotated

import requests
import json
import math

gpt4o_llm_config = {
    "config_list": [{"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")}]
}

claude_llm_config = {
    "config_list": [
        {
            "model": "claude-3-5-sonnet-20240620",
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "api_type": "anthropic",
        }
    ]
}


# define a function as a tool
def get_weather(location: Annotated[str, "Houston"]) -> str:
    """Retrieves the current weather data in a given city using the OpenWeatherMap API.

    Args:
        location (str): The name of the location to get the weather for.
        units (str): use metric for Celsius, imperial for Fahrenheit.

    Returns:
        int: The current weather in degrees Celsius. Returns None if an error occurs.
    """

    params = {
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "q": location,
        "units": "imperial",
    }

    OPENWEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(OPENWEATHER_API_BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for error status codes

        data = response.json()
        # print("WEATHER DATA: ", json.dumps(data))

        structured_data = {
            "city": location,
            "country_code": data["sys"]["country"],
            "summary": ". ".join([x["main"] for x in data["weather"]]),
            "description": ". ".join([x["description"] for x in data["weather"]]),
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "temp_max": math.ceil(data["main"]["temp_max"]),
            "temp_min": math.floor(data["main"]["temp_min"]),
            "humidity": round(data["main"]["humidity"]),
            "visibility": data["visibility"],
            "wind_speed": round(data["wind"]["speed"]),
            # data["wind"]["deg"]
        }

        if "rain" in data.keys():
            structured_data["rain_1h"] = data["rain"]["1h"]

        return structured_data

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        raise Exception(f"Weather data not available at this location: {location}")


meteorologist = ConversableAgent(
    "meteorologist",
    system_message="you are a meteorologist. "
        + " Use your weather knowledge and language skills to describe the weather condition."
        + " You must either Celsius or Fahrenheit according to the local custom. Do NOT use both units. ",
    human_input_mode="NEVER",
    llm_config=claude_llm_config,
)

user_proxy = ConversableAgent(
    "user_proxy",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None
    and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

register_function(
    get_weather,
    caller=meteorologist,
    executor=user_proxy,
    name="get_weather",
    description="get weather at a given location",
)

user_proxy.initiate_chat(
    meteorologist,
    # --> This message causes an infinite loop
    # This answer is more descriptive.
    message="What's the weather like in London?",
    # --> This message gets a short answer, exactly the same as the function return.
    # message="Tell me the weather in Houston and then say TERMINATE",
    max_turns=2,
)
