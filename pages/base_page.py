"""
Base Page Object Model class
"""

import logging
from typing import Optional
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO)


class BasePage:
    """Base page class that all page objects inherit from"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def find_element(self, locator: str, timeout: int = 10) -> Optional[object]:
        """Find element with explicit wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            return None
    
    def find_element_visible(self, locator: str, timeout: int = 10) -> Optional[object]:
        """Find visible element with explicit wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible: {locator}")
            return None
    
    def click_element(self, locator: str, timeout: int = 10) -> bool:
        """Click element with explicit wait"""
        element = self.find_element_visible(locator, timeout)
        if element:
            element.click()
            return True
        return False
    
    def enter_text(self, locator: str, text: str, timeout: int = 10) -> bool:
        """Enter text into element with explicit wait"""
        element = self.find_element(locator, timeout)
        if element:
            element.clear()
            element.send_keys(text)
            return True
        return False
    
    def get_text(self, locator: str, timeout: int = 10) -> Optional[str]:
        """Get text from element with explicit wait"""
        element = self.find_element_visible(locator, timeout)
        if element:
            return element.text.strip()
        return None
    
    def is_element_present(self, locator: str, timeout: int = 5) -> bool:
        """Check if element is present"""
        element = self.find_element(locator, timeout)
        return element is not None
    
    def is_element_visible(self, locator: str, timeout: int = 5) -> bool:
        """Check if element is visible"""
        element = self.find_element_visible(locator, timeout)
        return element is not None
    
    def wait_for_url_contains(self, url_fragment: str, timeout: int = 10) -> bool:
        """Wait for URL to contain specific fragment"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: url_fragment in driver.current_url
            )
            return True
        except TimeoutException:
            self.logger.error(f"URL did not contain '{url_fragment}' within {timeout}s")
            return False
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def navigate_to(self, url: str) -> None:
        """Navigate to specific URL"""
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")
    
    def refresh_page(self) -> None:
        """Refresh current page"""
        self.driver.refresh()
        self.logger.info("Page refreshed")
