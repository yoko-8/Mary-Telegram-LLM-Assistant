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
            weather_info = (
                f"\ntemperature: {data['main']['temp']}\n"
                f"temperature_min: {data['main']['temp_min']}\n"
                f"temperature_max: {data['main']['temp_max']}\n"
                f"weather_description: {data['weather'][0]['description']}\n"
                f"humidity: {data['main']['humidity']}\n"
                f"wind_speed: {data['wind']['speed']} mph\n"
            )
            return weather_info

    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")


def forecast_info(data, range):
    return (f"\n{data['list'][range]['dt_txt'].split()[0]}\n"
            f"time: {data['list'][range]['dt_txt'].split()[1]}\n"
            f"temperature: {data['list'][range]['main']['temp']}f\n"
            f"weather_description: {data['list'][range]['weather'][0]['description']}\n"
            f"humidity: {data['list'][range]['main']['humidity']}\n"
            f"wind_speed: {data['list'][range]['wind']['speed']} mph\n")


def weather_tomorrow():
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params)
        data = response.json()

        if response.status_code == 200:
            weather_tomorrow = forecast_info(data, 0)
            return weather_tomorrow

    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")


def forecast():
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params)
        data = response.json()

        if response.status_code == 200:
            x = None
            start_time = data["list"][0]["dt_txt"].split()[1]
            # print("START TIME IS: ", start_time)

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

            forecast_results = ''
            forecast_ranges = [0, 1, 3, 8, 9, 11, 16, 17, 19, 24, 25, 27, 32, 33]

            for forecast_range in forecast_ranges:
                forecast_results += forecast_info(data, forecast_range)
            return forecast_results

    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    print("Weather today is: ", weather_today())
    # print("Weather tomorrow is: ", weather_tomorrow())
    # print("Forecast for next 5 days is:", forecast())
