"""
Login Page Object Model
"""

from typing import Optional
from pages.base_page import BasePage
from features.locators import Locators


class LoginPage(BasePage):
    """Page Object Model for the SauceDemo login page"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/"
    
    def navigate_to_login_page(self) -> None:
        """Navigate to the login page"""
        self.navigate_to(self.url)
        self.logger.info("Navigated to login page")
    
    def is_login_page_loaded(self) -> bool:
        """Check if login page is loaded"""
        return (
            self.url in self.get_current_url() and 
            self.is_element_present(Locators.LOGIN_BUTTON)
        )
    
    def enter_username(self, username: str) -> bool:
        """Enter username in the username field"""
        return self.enter_text(Locators.USERNAME_FIELD, username)
    
    def enter_password(self, password: str) -> bool:
        """Enter password in the password field"""
        return self.enter_text(Locators.PASSWORD_FIELD, password)
    
    def click_login_button(self) -> bool:
        """Click the login button"""
        return self.click_element(Locators.LOGIN_BUTTON)
    
    def login(self, username: str, password: str) -> bool:
        """Perform complete login process"""
        self.logger.info(f"Attempting login with username: {username}")
        
        # Enter credentials
        username_success = self.enter_username(username)
        password_success = self.enter_password(password)
        
        if not (username_success and password_success):
            self.logger.error("Failed to enter credentials")
            return False
        
        # Click login button
        return self.click_login_button()
    
    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_element_present(Locators.ERROR_MESSAGE_CONTAINER, timeout=3)
    
    def get_error_message(self) -> Optional[str]:
        """Get the error message text"""
        if self.is_error_message_displayed():
            # Use the generic error container to get the text
            error_text = self.get_text(Locators.ERROR_MESSAGE_CONTAINER, timeout=2)
            if error_text:
                # Clean up the text by removing any button text or extra whitespace
                # The error text might include the close button, so we need to extract just the error message
                lines = error_text.strip().split('\n')
                for line in lines:
                    if 'Epic sadface:' in line:
                        return line.strip()
                return error_text.strip()
        
        return None
    
    def clear_credentials(self) -> None:
        """Clear username and password fields"""
        self.enter_username("")
        self.enter_password("")
        self.logger.info("Cleared credentials")
    
    def is_login_successful(self) -> bool:
        """Check if login was successful by checking URL and page elements"""
        # Wait for URL change to inventory page
        url_success = self.wait_for_url_contains("inventory.html", timeout=10)
        
        if url_success:
            # Verify product page title is present
            return self.is_element_present(Locators.PRODUCT_PAGE, timeout=5)
        
        return False
