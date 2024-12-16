"""
This module contains the Selenium env setup.
"""

import logging
from webdriver_manager.chrome import ChromeDriverManager


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

        context.browser = webdriver.Chrome(ChromeDriverManager().install())
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