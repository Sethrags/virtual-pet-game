# Filename: weatherapp.py
# Author: Evan
# Description: This file implements a simple weather application that fetches current weather data 
# for a given location using the wttr.in API. The application classifies the temperature into 
# categories (cold, temperate, hot) and returns the weather information in a structured format. 
# This can be used to provide weather-based interactions in the Tamagotchi game, such as changing 
# the pet's mood or behavior based on the current weather conditions. 
import requests

# classify_temp
# This function takes a temperature in Fahrenheit as input and classifies it into three categories:
# - "cold" for temperatures below 32°F
# - "temperate" for temperatures between 32°F and 95°F (inclusive)
# - "hot" for temperatures above 95°F
def classify_temp(temp_f):
    temp_f = float(temp_f)
    if temp_f < 32:
        return "cold"
    if temp_f <= 95:
        return "temperate"
    if temp_f > 95:
        return "hot"

# get_weather
# This function takes a location (city name) as input and fetches the current weather data from the wttr.in API. 
# It returns a dictionary containing the location, temperature, weather description, and temperature category. 
# If the API request fails, it returns None.
def get_weather(location):
    url = f"https://wttr.in/{location}?format=j1"
    response = requests.get(url)

    # Check if the API request was successful (status code 200)
    if response.status_code == 200: # has internet connection
        data = response.json()

        # Extract relevant weather information from the API response
        current = data["current_condition"][0] 
        temp = current["temp_F"]
        desc = current["weatherDesc"][0]["value"]
        # humidity = current["humidity"]
        # wind = current["windspeedKmph"]
        category = classify_temp(temp)

        # Return the weather information in a structured format (dictionary)
        return {
            "location": location,
            "temp": temp,
            "desc": desc,
            "category": category
        }
    else:
        return None # Return None if the API request fails (e.g., no internet connection or invalid location)


# Main block to test the get_weather function
# This block prompts the user to enter a city name, calls the get_weather function with the provided location,
if __name__ == "__main__":
    location = input("Please enter a city: ")
    get_weather(location)