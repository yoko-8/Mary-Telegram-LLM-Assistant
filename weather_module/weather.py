import os
import requests
from dotenv import load_dotenv

load_dotenv()
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "location.txt")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def read_location():
    try:
        with open(file_path, 'r') as file:
            return str(file.read())
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as error:
        print(f"An error occurred while reading the file: {str(error)}")


location = read_location()
params = {
    "q": location,
    "appid": WEATHER_API_KEY,
    "units": "imperial"
}


def write_location(location):
    try:
        with open(file_path, 'w') as file:
            file.write(location)
            print(f"Location '{location}' has been written to the file.")
    except Exception as error:
        print(f"An error occurred while writing to the file: {str(error)}")


def get_weather(sentence):
    if "tomorrow" in sentence or "tmrw" in sentence or "tmr" in sentence:
        return weather_tomorrow()
    elif "week" in sentence or "future" in sentence:
        return forecast()
    else:
        return weather_today()


def weather_today():
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params)
        data = response.json()

        if response.status_code == 200:
            weather_info = {
                "temperature": data["main"]["temp"],
                "temperature_min": data["main"]["temp_min"],
                "temperature_max": data["main"]["temp_max"],
                "weather_description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": str(data["wind"]["speed"]) + " mph",
            }
            return weather_info

    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")


def weather_tomorrow():
    forecast_info = forecast()
    tomorrow_date = next(iter(forecast_info))
    return forecast_info[tomorrow_date]


def forecast():
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params)
        data = response.json()

        if response.status_code == 200:
            x = None
            start_time = data["list"][0]["dt_txt"].split()[1]
            print("START TIME IS: ", start_time)

            if start_time == "00:00:00":
                x = 3
            elif start_time == "03:00:00":
                x = 2
            elif start_time == "06:00:00":
                x = 1
            elif start_time == "09:00:00":
                x = 0
            elif start_time == "12:00:00":
                x = 1
            elif start_time == "15:00:00":
                x = 2
            elif start_time == "18:00:00":
                x = 3
            elif start_time == "21:00:00":
                x = 4

            forecast_info = {
                data["list"][x]["dt_txt"].split()[0]: {
                    data["list"][x]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x]["main"]["temp"],
                        "weather_description": data["list"][x]["weather"][0]["description"],
                        "humidity": data["list"][x]["main"]["humidity"],
                        "wind_speed": str(data["list"][x]["wind"]["speed"]) + " mph"
                    },
                    data["list"][x + 1]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 1]["main"]["temp"],
                        "weather_description": data["list"][x + 1]["weather"][0]["description"],
                        "humidity": data["list"][x + 1]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 1]["wind"]["speed"]) + " mph"
                    },
                    data["list"][x + 3]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 3]["main"]["temp"],
                        "weather_description": data["list"][x + 3]["weather"][0]["description"],
                        "humidity": data["list"][x + 3]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 3]["wind"]["speed"]) + " mph"
                    },
                },
                data["list"][x + 8]["dt_txt"].split()[0]: {
                    data["list"][x + 8]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 8]["main"]["temp"],
                        "weather_description": data["list"][x + 8]["weather"][0]["description"],
                        "humidity": data["list"][x + 8]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 8]["wind"]["speed"]) + " mph"
                    },
                    data["list"][x + 9]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 9]["main"]["temp"],
                        "weather_description": data["list"][x + 9]["weather"][0]["description"],
                        "humidity": data["list"][x + 9]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 9]["wind"]["speed"]) + " mph"
                    },
                    data["list"][x + 11]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 11]["main"]["temp"],
                        "weather_description": data["list"][x + 11]["weather"][0]["description"],
                        "humidity": data["list"][x + 11]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 11]["wind"]["speed"]) + " mph"
                    },
                },
                data["list"][x + 16]["dt_txt"].split()[0]: {
                    data["list"][x + 16]["dt_txt"].split()[1]: {
                        "temperature": data["list"][16]["main"]["temp"],
                        "weather_description": data["list"][16]["weather"][0]["description"],
                        "humidity": data["list"][x + 16]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 16]["wind"]["speed"]) + " mph"
                    },
                    data["list"][x + 17]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 17]["main"]["temp"],
                        "weather_description": data["list"][x + 17]["weather"][0]["description"],
                        "humidity": data["list"][x + 17]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 17]["wind"]["speed"]) + " mph"
                    },
                    data["list"][x + 19]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 19]["main"]["temp"],
                        "weather_description": data["list"][x + 19]["weather"][0]["description"],
                        "humidity": data["list"][x + 19]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 19]["wind"]["speed"]) + " mph"
                    },
                },
                data["list"][x + 24]["dt_txt"].split()[0]: {
                    data["list"][x + 24]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 24]["main"]["temp"],
                        "weather_description": data["list"][x + 24]["weather"][0]["description"],
                        "humidity": data["list"][x + 24]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 24]["wind"]["speed"]) + " mph"
                    },
                    data["list"][x + 25]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 25]["main"]["temp"],
                        "weather_description": data["list"][x + 25]["weather"][0]["description"],
                        "humidity": data["list"][x + 25]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 25]["wind"]["speed"]) + " mph"
                    },
                    data["list"][x + 27]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 27]["main"]["temp"],
                        "weather_description": data["list"][x + 27]["weather"][0]["description"],
                        "humidity": data["list"][x + 27]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 27]["wind"]["speed"]) + " mph"
                    },
                },
                data["list"][x + 32]["dt_txt"].split()[0]: {
                    data["list"][x + 32]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 32]["main"]["temp"],
                        "weather_description": data["list"][x + 32]["weather"][0]["description"],
                        "humidity": data["list"][x + 32]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 32]["wind"]["speed"]) + " mph"
                    },
                    data["list"][x + 33]["dt_txt"].split()[1]: {
                        "temperature": data["list"][x + 33]["main"]["temp"],
                        "weather_description": data["list"][x + 33]["weather"][0]["description"],
                        "humidity": data["list"][x + 33]["main"]["humidity"],
                        "wind_speed": str(data["list"][x + 33]["wind"]["speed"]) + " mph"
                    },
                }
            }
            return forecast_info

    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    print("Weather today is: ", weather_today())
    print("Weather tomorrow is: ", weather_tomorrow())
    print("Forecast for next 5 days is:", forecast())
