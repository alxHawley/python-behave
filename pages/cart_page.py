"""
Cart Page Object Model
"""

from typing import Optional
from pages.base_page import BasePage
from features.locators import Locators


class CartPage(BasePage):
    """Page Object Model for the SauceDemo cart page"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_cart_page_loaded(self) -> bool:
        """Check if cart page is loaded"""
        return (
            "cart" in self.get_current_url().lower() and
            self.is_element_present(Locators.CART_PAGE_TITLE)
        )
    
    def get_cart_page_title(self) -> Optional[str]:
        """Get the cart page title"""
        return self.get_text(Locators.CART_PAGE_TITLE)
    
    def is_correct_cart_title(self) -> bool:
        """Check if cart page title is 'Your Cart'"""
        title = self.get_cart_page_title()
        return title == "Your Cart" if title else False
    
    def is_product_in_cart(self, product_name: str) -> bool:
        """Check if a specific product is in the cart"""
        cart_item_locator = Locators.cart_item(product_name)
        return self.is_element_present(cart_item_locator)
    
    def get_cart_item_text(self, product_name: str) -> Optional[str]:
        """Get the text of a cart item"""
        cart_item_locator = Locators.cart_item(product_name)
        return self.get_text(cart_item_locator)
    
    def click_checkout_button(self) -> bool:
        """Click the checkout button"""
        return self.click_element(Locators.CHECKOUT_BUTTON)
    
    def verify_cart_contents(self, product_name: str) -> bool:
        """Verify that a product is in the cart with correct title"""
        if not self.is_cart_page_loaded():
            self.logger.error("Cart page not loaded")
            return False
        
        if not self.is_correct_cart_title():
            self.logger.error("Incorrect cart page title")
            return False
        
        if not self.is_product_in_cart(product_name):
            self.logger.error(f"Product '{product_name}' not found in cart")
            return False
        
        return True
