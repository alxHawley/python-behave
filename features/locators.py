"""Locators for UI tests"""


class Locators:
    """Class to store locators for web elements"""

    # Checkout Flow Locators
    FIRST_NAME = "//input[@id='first-name']"
    LAST_NAME = "//input[@id='last-name']"
    POSTAL_CODE = "//input[@id='postal-code']"
    CHECKOUT_BUTTON = "//button[@id='checkout']"
    # update: ADD_TO_CART_BUTTON to be dynamic xpath selector
    ADD_TO_CART_BUTTON = "//button[@id='add-to-cart-sauce-labs-backpack']"
    # update: CART_ITEM to be dynamic xpath selector
    CART_ITEM = "//div[text()='Sauce Labs Backpack']"
    CHECKOUT_INFO = "//div[@id='checkout_info_container']"

    # Nav Locators
    CANCEL_BUTTON = "//button[@id='cancel']"
    CART_ICON = "//a[@class='shopping_cart_link']"
    CONTINUE_BUTTON = "//input[@id='continue']"
    # CON_SHOPPING_BUTTON
    # ERROR_MESSAGE
    # FOOTER_TEXT
    FINISH_BUTTON = "//button[@id='finish']"
    # PRODUCT_SORT_DROPDOWN
    # REACT_BURGER
    # SIDEBAR_LINKS
    # SOCIAL_LINKS

    # Login Locators
    # LOGIN_BUTTON
    # PASSWORD_FIELD
    # USERNAME_FIELD
