from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from jsonschema import validate
import json


# page title assert test
def test_get_title():
    driver = webdriver.Chrome()
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    print(driver.title)
    assert driver.title == "Web form"
    driver.quit()


# find search bar and send keys test
def test_element_find():
    driver = webdriver.Chrome()
    driver.get("https://www.python.org")
    print(driver.title)
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.clear()
    search_bar.send_keys("getting started with python")
    search_bar.send_keys(Keys.RETURN)
    print(driver.current_url)
    driver.close()


# api response test
def test_api_response():
    response = requests.get("https://catfact.ninja/fact")
    print(response.status_code)
    assert response.status_code == 200
    print(response.headers.get("Content-Type"))
    print(response.headers.get("Date"))
    print(response.json())


# api schema validation test
def test_schema():
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?"
                            "lat=47.6488&lon=-122.3964&appid=f82534b2ff8f9e2c2b0536a99e0d8c87")
    
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "application/json; charset=utf-8"
    with open('schemas/weather.json', 'r') as f:
        weather_schema = json.loads(f.read())
    weather_data = response.json()
    validate(instance=weather_data, schema=weather_schema)
