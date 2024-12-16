"""
This module contains the Selenium env setup.
"""

import logging


def before_all(context):
    """Setup logging"""
    logging.basicConfig(level=logging.INFO)


def before_scenario(context, scenario):
    """Setup chrome browser if running UI tests"""
    if "ui" in scenario.effective_tags:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service

        # Set Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        try:
            # Try to use webdriver_manager
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        except ImportError:
            # Fallback to local ChromeDriver path
            service = Service(
                "C:/Program Files/Google/Chrome/Driver/chromedriver.exe"
            )

        context.browser = webdriver.Chrome(
            service=service, options=chrome_options
        )
        context.browser.maximize_window()


def after_scenario(context, scenario):
    """Close chrome browser if running UI tests"""
    if "ui" in scenario.effective_tags and hasattr(context, "browser"):
        context.browser.quit()
