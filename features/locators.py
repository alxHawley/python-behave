"""Locators for UI tests"""


class Locators:
    """Class stores all the locators for the application"""

    # Static methods for dynamic locators
    @staticmethod
    def cart_item(product_name):
        return f"//div[text()='{product_name}']"

    @staticmethod
    def add_to_cart_button(product_name):
        return (
            f"//button[contains(@id, 'add-to-cart-"
            f"{product_name.lower().replace(' ', '-')}')]"
        )

    # Login Locators
    LOGIN_BUTTON = "//input[@id='login-button']"
    USERNAME_FIELD = "//input[@id='user-name']"
    PASSWORD_FIELD = "//input[@id='password']"

    # Page Locators
    PRODUCT_PAGE = "//span[@class='title' and text()='Products']"
    CHECKOUT_PAGE = (
        "//span[@class='title' and text()='Checkout: Your Information']"
    )
    CART_PAGE_TITLE = "//span[@class='title' and text()='Your Cart']"
    CHECKOUT_OVERVIEW = (
        "//span[@class='title' and text()='Checkout: Overview']")
    CHECKOUT_COMPLETE = (
        "//span[@class='title' and text()='Checkout: Complete!']")

    # Checkout Flow Locators
    FIRST_NAME = "//input[@id='first-name']"
    LAST_NAME = "//input[@id='last-name']"
    POSTAL_CODE = "//input[@id='postal-code']"
    CHECKOUT_BUTTON = "//button[@id='checkout']"

    # CART_REMOVE = "//button[@id='remove-sauce-labs-backpack']" # not used
    FINISH_BUTTON = "//button[@id='finish']"

    # Product Page Locators
    # PRODUCT_SORT_DROPDOWN = "//select[@class='product_sort_container']"
    # BACK_TO_PRODUCTS = "//button[@id='back-to-products']" # not used
    # PRODUCT_REMOVE = "//button[@id='remove']" # not used

    # Nav Locators
    CART_ICON = "//a[@class='shopping_cart_link']"
    # BACK_HOME = "//button[@id='back-to-products']" # not used
    # CANCEL_BUTTON = "//button[@id='cancel']" # not used
    CONTINUE_BUTTON = "//input[@id='continue']"
    # CON_SHOPPING_BUTTON = "//button[@id='continue-shopping']" # not used
    REACT_BURGER = "//button[@id='react-burger-menu-btn']"

    # ERROR_MESSAGES
    UN_PW_ERROR = (
        "//h3[contains(text(),'Epic sadface: Username and password do not "
        "match any user in this service')]"
    )
    LOCKED_OUT_ERROR = (
        "//h3[contains(text(),'Epic sadface: Sorry, this user has been "
        "locked out.')]"
    )

    # SIDEBAR_LINKS
    LOGOUT = "//a[@id='logout_sidebar_link']"
    # ALL_ITEMS = "//a[@id='inventory_sidebar_link']" # not implemented
    # ABOUT = "//a[@id='about_sidebar_link']" # not implemented
    # RESET_APP_STATE = "//a[@id='reset_sidebar_link']" # not implemented

    # SOCIAL_LINKS
