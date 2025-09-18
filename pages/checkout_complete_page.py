"""
Checkout Complete Page Object Model
"""

from typing import Optional
from pages.base_page import BasePage
from features.locators import Locators


class CheckoutCompletePage(BasePage):
    """Page Object Model for the SauceDemo checkout complete page"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_complete_page_loaded(self) -> bool:
        """Check if checkout complete page is loaded"""
        return (
            "checkout-complete" in self.get_current_url() and
            self.is_element_present(Locators.CHECKOUT_COMPLETE)
        )
    
    def get_complete_page_title(self) -> Optional[str]:
        """Get the checkout complete page title"""
        return self.get_text(Locators.CHECKOUT_COMPLETE)
    
    def is_correct_complete_title(self) -> bool:
        """Check if complete page title is 'Checkout: Complete!'"""
        title = self.get_complete_page_title()
        return title == "Checkout: Complete!" if title else False
    
    def verify_complete_page(self) -> bool:
        """Verify that checkout complete page is loaded correctly"""
        if not self.is_complete_page_loaded():
            self.logger.error("Checkout complete page not loaded")
            return False
        
        if not self.is_correct_complete_title():
            self.logger.error("Incorrect complete page title")
            return False
        
        return True
