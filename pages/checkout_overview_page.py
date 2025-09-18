"""
Checkout Overview Page Object Model
"""

from typing import Optional
from pages.base_page import BasePage
from features.locators import Locators


class CheckoutOverviewPage(BasePage):
    """Page Object Model for the SauceDemo checkout overview page"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_overview_page_loaded(self) -> bool:
        """Check if checkout overview page is loaded"""
        return (
            "checkout-step-two" in self.get_current_url() and
            self.is_element_present(Locators.CHECKOUT_OVERVIEW)
        )
    
    def get_overview_page_title(self) -> Optional[str]:
        """Get the checkout overview page title"""
        return self.get_text(Locators.CHECKOUT_OVERVIEW)
    
    def is_correct_overview_title(self) -> bool:
        """Check if overview page title is 'Checkout: Overview'"""
        title = self.get_overview_page_title()
        return title == "Checkout: Overview" if title else False
    
    def click_finish_button(self) -> bool:
        """Click the finish button"""
        return self.click_element(Locators.FINISH_BUTTON)
    
    def verify_overview_page(self) -> bool:
        """Verify that checkout overview page is loaded correctly"""
        if not self.is_overview_page_loaded():
            self.logger.error("Checkout overview page not loaded")
            return False
        
        if not self.is_correct_overview_title():
            self.logger.error("Incorrect overview page title")
            return False
        
        return True
