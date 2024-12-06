"""
This module contains the Selenium env setup.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def before_all(context):
    """Setup chrome browser"""
    service = Service("C:/Program Files/Google/Chrome/Application/chromedriver.exe")
    context.browser = webdriver.Chrome(service=service)
    context.browser.maximize_window()


def after_all(context):
    """Close chrome browser"""
    context.browser.quit()
