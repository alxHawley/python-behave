"""
Page Factory for creating page objects
"""

from typing import Optional
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage


class PageFactory:
    """Factory class for creating page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self._login_page = None
        self._product_page = None
        self._cart_page = None
        self._checkout_page = None
        self._checkout_overview_page = None
        self._checkout_complete_page = None
    
    @property
    def login_page(self) -> LoginPage:
        """Get or create LoginPage instance"""
        if self._login_page is None:
            self._login_page = LoginPage(self.driver)
        return self._login_page
    
    @property
    def product_page(self) -> ProductPage:
        """Get or create ProductPage instance"""
        if self._product_page is None:
            self._product_page = ProductPage(self.driver)
        return self._product_page
    
    @property
    def cart_page(self) -> CartPage:
        """Get or create CartPage instance"""
        if self._cart_page is None:
            self._cart_page = CartPage(self.driver)
        return self._cart_page
    
    @property
    def checkout_page(self) -> CheckoutPage:
        """Get or create CheckoutPage instance"""
        if self._checkout_page is None:
            self._checkout_page = CheckoutPage(self.driver)
        return self._checkout_page
    
    @property
    def checkout_overview_page(self) -> CheckoutOverviewPage:
        """Get or create CheckoutOverviewPage instance"""
        if self._checkout_overview_page is None:
            self._checkout_overview_page = CheckoutOverviewPage(self.driver)
        return self._checkout_overview_page
    
    @property
    def checkout_complete_page(self) -> CheckoutCompletePage:
        """Get or create CheckoutCompletePage instance"""
        if self._checkout_complete_page is None:
            self._checkout_complete_page = CheckoutCompletePage(self.driver)
        return self._checkout_complete_page
    
    def get_page_by_url(self, url: str) -> Optional[object]:
        """Get appropriate page object based on current URL"""
        if "saucedemo.com" in url and "inventory" not in url and "cart" not in url and "checkout" not in url:
            return self.login_page
        elif "inventory.html" in url:
            return self.product_page
        elif "cart" in url.lower():
            return self.cart_page
        elif "checkout-step-one" in url:
            return self.checkout_page
        elif "checkout-step-two" in url:
            return self.checkout_overview_page
        elif "checkout-complete" in url:
            return self.checkout_complete_page
        else:
            return None
