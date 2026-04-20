import requests

# feel free to adjust these values if you need to
def classify_temp(temp_f):
    temp_f = float(temp_f)
    if temp_f < 32:
        return "cold"
    if temp_f <= 100:
        return "temperate"
    if temp_f > 100:
        return "hot"

def get_weather(location):
    url = f"https://wttr.in/{location}?format=j1"
    response = requests.get(url)

    if response.status_code == 200: # has internet connection
        data = response.json()

        # conditions
        current = data["current_condition"][0]
        temp = current["temp_F"]
        desc = current["weatherDesc"][0]["value"]
        # humidity = current["humidity"]
        # wind = current["windspeedKmph"]
        category = classify_temp(temp)

        return {
            "location": location,
            "temp": temp,
            "desc": desc,
            "category": category
        }
    else:
        return None

# tests
'''
        print(f"\nWeather in {location.capitalize()}:")
        print(f"Temperature: {temp} F {category}")
        print(f"Conditions: {desc}")
    else:
        print("Weather data not found")
'''
if __name__ == "__main__":
    location = input("Please enter a city: ")
    get_weather(location)