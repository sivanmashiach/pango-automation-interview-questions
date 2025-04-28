import pprint

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_timeanddate_weather():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.timeanddate.com/weather/"
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//table")))

    weather_dict = {}

    for i in range(1, 21):
        city_xpath = f"//table//tbody/tr[{i}]/td[1]/a"
        city_element = driver.find_element(By.XPATH, city_xpath)
        city_name = city_element.text

        temp_xpath = f"//table//tbody/tr[{i}]/td[4]"
        temp_element = driver.find_element(By.XPATH, temp_xpath)
        temperature = temp_element.text.split('°')[0].strip()

        weather_dict[city_name] = int(temperature)

    driver.quit()

    return weather_dict


if __name__ == '__main__':
    weather_data = extract_timeanddate_weather()
    pprint.pprint(weather_data)
