import requests

API_key="aa80c320c5f4d62b89e95aab6345b411"

def get_data(place, forecast_days=None):
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_key}"
        response = requests.get(url)
        data = response.json()
        filtered_data = data["list"]
        nr_values = 8 * forecast_days
        filtered_data = filtered_data[:nr_values]
        return filtered_data

if __name__ == "__main__":
        print(get_data(place="cambodia", forecast_days=3))