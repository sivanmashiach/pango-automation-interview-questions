import sqlite3
import os

from automation_framework.utilities.api_helpers import ApiHelper
from automation_framework.utilities.config_helpers import get_db_name
from automation_framework.utilities.test_cities import cities


class DatabaseHelper:
    def __init__(self, db_name=get_db_name()):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        # Create tables if they don't exist
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                city TEXT PRIMARY KEY,
                temperature REAL,
                feels_like REAL,
                average_temperature REAL
            )''')

    def insert_weather_data(self, city, temperature, feels_like, temp_avg):
        with self.conn:
            self.conn.execute(f'''
                INSERT OR REPLACE INTO weather_data (city, temperature, feels_like, average_temperature)
                VALUES (?, ?, ?, ?)
            ''', (city, temperature, feels_like, temp_avg))

    def get_weather_data(self, city):
        with self.conn:
            result = self.conn.execute('''
                SELECT city, temperature, feels_like, average_temperature
                FROM weather_data
                WHERE city = ?
            ''', (city,))
            return result.fetchone()

    def get_city_with_highest_avg(self):
        with self.conn:
            result = self.conn.execute('''
                SELECT city
                FROM weather_data
                ORDER BY average_temperature DESC
                LIMIT 1
            ''')
            return result.fetchone()

    def delete_db(self):
        self.conn.close()
        os.remove("data.db")

    def populate_db(self, api):
        for city in cities:
            response = api.get_current_weather(city)
            temp = response["main"]["temp"]
            feels_like = response["main"]["feels_like"]
            temp_min = response["main"]["temp_min"]
            temp_max = response["main"]["temp_max"]
            temp_avg = (temp_min + temp_max) / 2
            self.insert_weather_data(city, temp, feels_like, temp_avg)

if __name__ == '__main__':
    DatabaseHelper().populate_db(ApiHelper())