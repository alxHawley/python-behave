"""
This module contains the Selenium env setup.
"""

import logging
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def before_all(context):
    """Setup logging"""
    logging.basicConfig(level=logging.INFO)
    logging.info("before_all: Logging setup complete")


def before_scenario(context, scenario):
    """Setup chrome browser if running UI tests"""
    logging.info(
        f"before_scenario: Running scenario '{scenario.name}' "
        f"with tags {scenario.effective_tags}'"
    )
    if "ui" in scenario.effective_tags:
        from selenium import webdriver

        # Create a Service object with the path to the ChromeDriver
        service = Service(ChromeDriverManager().install())
        context.browser = webdriver.Chrome(service=service)
        context.browser.maximize_window()
        logging.info("before_scenario: Browser setup complete")


def after_scenario(context, scenario):
    """Close chrome browser if running UI tests"""
    logging.info(
        f"after_scenario: Running scenario '{scenario.name}' "
        f"with tags {scenario.effective_tags}"
    )
    if "ui" in scenario.effective_tags and hasattr(context, "browser"):
        context.browser.quit()
        logging.info("after_scenario: Browser closed")