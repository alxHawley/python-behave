"""
Selenium steps for 'e2e.feature'
"""

import logging

# pylint: disable=no-name-in-module
from behave import then, when

# pylint: enable=no-name-in-module
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from features.locators import Locators

logging.basicConfig(level=logging.INFO)


@when("the user adds a product to the cart")
def step_add_to_cart(context):
    """Add a product to the cart"""
    add_product_button = WebDriverWait(context.browser, 3).until(
        EC.presence_of_element_located((By.XPATH, Locators.ADD_TO_CART_BUTTON))
    )
    add_product_button.click()


@when("the user clicks on the cart icon")
def step_click_cart(context):
    """Click on the cart icon"""
    cart_button = WebDriverWait(context.browser, 3).until(
        EC.presence_of_element_located((By.XPATH, Locators.CART_ICON))
    )
    cart_button.click()


@then("the user is able to see the item in the cart")
def step_verify_cart(context):
    """Verify that the item is in the cart"""
    cart_item = context.browser.find_element(By.XPATH, Locators.CART_ITEM)
    assert cart_item is not None, "Item not found in cart"
    # add an assert to veritfy page title rel xpath text = "Your Cart"


@when("the user clicks on the checkout button")
def step_click_checkout(context):
    """Click on the checkout button"""
    checkout_button = context.browser.find_element(By.XPATH, Locators.CHECKOUT_BUTTON)
    checkout_button.click()


@then("the user is able to see the checkout page")  # Rewrite this
def step_verify_checkout(context):
    """Verify that the checkout page is displayed"""
    try:
        checkout_info = WebDriverWait(context.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, Locators.CHECKOUT_INFO))
        )
        assert checkout_info is not None, "Checkout page not found"
    except TimeoutException:
        assert False, "Checkout page not found within the given time"


@when("the user fills the form with the following data")
def step_fill_checkout(context):
    """Fill the checkout form"""
    for row in context.table:
        first_name = context.browser.find_element(By.XPATH, Locators.FIRST_NAME)
        last_name = context.browser.find_element(By.XPATH, Locators.LAST_NAME)
        postal_code = context.browser.find_element(By.XPATH, Locators.POSTAL_CODE)

        first_name.send_keys(row["First Name"])
        last_name.send_keys(row["Last Name"])
        postal_code.send_keys(row["Zip/Postal Code"])


@when("the user clicks on the continue button")  # Rewrite this
def click_continue(context):
    """Click on the continue button"""
    continue_button = context.browser.find_element(By.XPATH, Locators.CONTINUE_BUTTON)
    continue_button.click()


@then("the user is able to see the overview page")  # rewrite this
def step_verify_overview(context):
    """Verify that the overview page is displayed"""
    assert (
        "https://www.saucedemo.com/checkout-step-two.html"
        in context.browser.current_url
    ), "Not on the overview page"


@when("the user clicks on the finish button")
def step_click_finish(context):
    """Click on the finish button"""
    finish_button = context.browser.find_element(By.XPATH, Locators.FINISH_BUTTON)
    finish_button.click()


@then("the user is able to see the confirmation page")
def step_verify_confirmation(context):
    """Verify that the confirmation page is displayed"""
    assert (
        "https://www.saucedemo.com/checkout-complete.html"
        in context.browser.current_url
    ), "Not on the confirmation page"
