import requests

from automation_framework.utilities.config_helpers import get_api_key, get_base_url


class ApiHelper:
    BASE_URL = get_base_url()
    API_KEY = get_api_key()

    def get_current_weather(self, city):
        url = f"{self.BASE_URL}?q={city}&appid={self.API_KEY}&units=metric"
        response = requests.get(url)
        return response.json()
