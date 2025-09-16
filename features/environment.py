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
        chrome_options.add_argument("--headless")  # Enable headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--no-proxy-server")
        
        # Disable password save popup and leak detection
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        chrome_options.add_experimental_option("prefs", prefs)

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
