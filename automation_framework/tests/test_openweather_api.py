import pytest
from automation_framework.utilities.api_helpers import ApiHelper
from automation_framework.utilities.db_helpers import DatabaseHelper
from automation_framework.utilities.test_cities import cities


@pytest.fixture(scope="module")
def api():
    return ApiHelper()


@pytest.fixture(scope="module")
def db(api):
    db_helper = DatabaseHelper()
    db_helper.populate_db(api)
    yield db_helper
    db_helper.delete_db()


def test_get_weather_data(api, db):
    for city in cities:
        response = api.get_current_weather(city)
        city_name, temp, feels_like, avg = db.get_weather_data(city)
        assert temp == response["main"]["temp"]
        assert feels_like == response["main"]["feels_like"]
        temp_min = response["main"]["temp_min"]
        temp_max = response["main"]["temp_max"]
        temp_avg = (temp_min + temp_max) / 2
        assert avg == temp_avg
    top_avg_city = db.get_city_with_highest_avg()[0]
    print(top_avg_city)
