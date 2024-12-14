"""
This module contains the Selenium env setup.
"""

import os


def before_all(context):
    """Setup chrome browser if running UI tests"""
    if os.getenv("RUN_UI_TESTS") == "true":
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service

        service = Service("C:/Program Files/Google/Chrome/Application/chromedriver.exe")
        context.browser = webdriver.Chrome(service=service)
        context.browser.maximize_window()


def after_all(context):
    """Close chrome browser if running UI tests"""
    if os.getenv("RUN_UI_TESTS") == "true" and hasattr(context, "browser"):
        context.browser.quit()
