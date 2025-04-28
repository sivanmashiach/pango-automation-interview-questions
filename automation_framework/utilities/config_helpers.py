from configparser import ConfigParser

config = ConfigParser()
config.read("automation_framework/config/config.ini")

def get_api_key():
    return config.get("API", "API_KEY")

def get_base_url():
    return config.get("API", "BASE_URL")

def get_db_name():
    return config.get("DB", "DB_NAME")
