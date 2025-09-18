"""
Product Page Object Model
"""

from typing import Optional
from pages.base_page import BasePage
from features.locators import Locators


class ProductPage(BasePage):
    """Page Object Model for the SauceDemo product/inventory page"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_product_page_loaded(self) -> bool:
        """Check if product page is loaded"""
        return (
            "inventory.html" in self.get_current_url() and
            self.is_element_present(Locators.PRODUCT_PAGE)
        )
    
    def get_page_title(self) -> Optional[str]:
        """Get the product page title"""
        return self.get_text(Locators.PRODUCT_PAGE)
    
    def is_correct_page_title(self) -> bool:
        """Check if page title is 'Products'"""
        title = self.get_page_title()
        return title == "Products" if title else False
    
    def open_navigation_menu(self) -> bool:
        """Open the navigation menu"""
        return self.click_element(Locators.REACT_BURGER)
    
    def click_logout(self) -> bool:
        """Click logout button in navigation menu"""
        return self.click_element(Locators.LOGOUT, timeout=2)
    
    def logout(self) -> bool:
        """Perform complete logout process"""
        self.logger.info("Performing logout")
        
        # Open navigation menu
        if not self.open_navigation_menu():
            self.logger.error("Failed to open navigation menu")
            return False
        
        # Click logout
        if not self.click_logout():
            self.logger.error("Failed to click logout button")
            return False
        
        return True
    
    def is_logged_out(self) -> bool:
        """Check if user is logged out (redirected to login page)"""
        return self.wait_for_url_contains("saucedemo.com/", timeout=10) and \
               "inventory" not in self.get_current_url()
    
    def wait_for_page_load(self, timeout: int = 5) -> bool:
        """Wait for inventory container to load (for performance testing)"""
        try:
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.common.by import By
            from selenium.common.exceptions import TimeoutException
            
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.ID, "inventory_container"))
            )
            return True
        except TimeoutException:
            self.logger.error(f"Inventory container did not load within {timeout}s")
            return False
    
    def add_product_to_cart(self, product_name: str) -> bool:
        """Add a product to the cart"""
        add_to_cart_locator = Locators.add_to_cart_button(product_name)
        self.logger.info(f"Adding product '{product_name}' to cart")
        return self.click_element(add_to_cart_locator)
    
    def click_cart_icon(self) -> bool:
        """Click on the cart icon"""
        self.logger.info("Clicking cart icon")
        success = self.click_element(Locators.CART_ICON)
        
        if success:
            # Wait for navigation to cart page
            return self.wait_for_url_contains("cart", timeout=10)
        
        return False
    
    def add_product_and_go_to_cart(self, product_name: str) -> bool:
        """Add product to cart and navigate to cart page"""
        if not self.add_product_to_cart(product_name):
            self.logger.error(f"Failed to add product '{product_name}' to cart")
            return False
        
        return self.click_cart_icon()
