"""
Checkout Page Object Model
"""

from typing import Optional, Dict
from pages.base_page import BasePage
from features.locators import Locators


class CheckoutPage(BasePage):
    """Page Object Model for the SauceDemo checkout page"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_checkout_page_loaded(self) -> bool:
        """Check if checkout page is loaded"""
        return (
            "checkout-step-one" in self.get_current_url() and
            self.is_element_present(Locators.CHECKOUT_PAGE)
        )
    
    def get_checkout_page_title(self) -> Optional[str]:
        """Get the checkout page title"""
        return self.get_text(Locators.CHECKOUT_PAGE)
    
    def is_correct_checkout_title(self) -> bool:
        """Check if checkout page title is correct"""
        title = self.get_checkout_page_title()
        return title == "Checkout: Your Information" if title else False
    
    def enter_first_name(self, first_name: str) -> bool:
        """Enter first name"""
        return self.enter_text(Locators.FIRST_NAME, first_name)
    
    def enter_last_name(self, last_name: str) -> bool:
        """Enter last name"""
        return self.enter_text(Locators.LAST_NAME, last_name)
    
    def enter_postal_code(self, postal_code: str) -> bool:
        """Enter postal code"""
        return self.enter_text(Locators.POSTAL_CODE, postal_code)
    
    def fill_checkout_form(self, checkout_data: Dict[str, str]) -> bool:
        """Fill the complete checkout form"""
        self.logger.info(f"Filling checkout form with data: {checkout_data}")
        
        first_name_success = self.enter_first_name(checkout_data.get("First Name", ""))
        last_name_success = self.enter_last_name(checkout_data.get("Last Name", ""))
        postal_code_success = self.enter_postal_code(checkout_data.get("Zip/Postal Code", ""))
        
        return first_name_success and last_name_success and postal_code_success
    
    def click_continue_button(self) -> bool:
        """Click the continue button"""
        return self.click_element(Locators.CONTINUE_BUTTON)
    
    def complete_checkout_form(self, checkout_data: Dict[str, str]) -> bool:
        """Complete the entire checkout form process"""
        if not self.fill_checkout_form(checkout_data):
            self.logger.error("Failed to fill checkout form")
            return False
        
        return self.click_continue_button()
    
    def verify_checkout_page(self) -> bool:
        """Verify that checkout page is loaded correctly"""
        if not self.is_checkout_page_loaded():
            self.logger.error("Checkout page not loaded")
            return False
        
        if not self.is_correct_checkout_title():
            self.logger.error("Incorrect checkout page title")
            return False
        
        return True
