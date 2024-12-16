"""
This module contains the Selenium env setup.
"""

import logging


def before_all(context):
    """Setup logging"""
    logging.basicConfig(level=logging.INFO)
    logging.info("before_all: Logging setup complete")


def before_scenario(context, scenario):
    """Setup chrome browser if running UI tests"""
    logging.info(
        f"before_scenario: Running scenario '{scenario.name}' "
        f"with tags {scenario.tags}'"
    )
    if "ui" in scenario.effective_tags:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service

        service = Service(
            "C:/Program Files/Google/Chrome/Application/chromedriver.exe"
        )
        context.browser = webdriver.Chrome(service=service)
        context.browser.maximize_window()
        logging.info("before_scenario: Browser setup complete")


def after_scenario(context, scenario):
    """Close chrome browser if running UI tests"""
    logging.info(
        f"after_scenario: Running scenario '{scenario.name}' "
        f"with tags {scenario.tags}"
    )
    if "ui" in scenario.tags and hasattr(context, "browser"):
        context.browser.quit()
        logging.info("after_scenario: Browser closed")