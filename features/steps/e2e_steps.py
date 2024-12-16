"""
Selenium steps for 'e2e.feature'
"""

import logging
import os

# pylint: disable=no-name-in-module
from behave import then, when

# pylint: enable=no-name-in-module
if os.getenv("RUN_UI_TESTS") == "true":
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

from features.locators import Locators

logging.basicConfig(level=logging.INFO)


@when('the user adds the product "{product_name}" to the cart')
def step_add_to_cart(context, product_name):
    """Add a product to the cart"""
    add_to_cart_button_xpath = Locators.add_to_cart_button(product_name)
    add_product_button = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, add_to_cart_button_xpath))
    )
    add_product_button.click()


@when("the user clicks on the cart icon")
def step_click_cart(context):
    """Click on the cart icon"""
    cart_button = WebDriverWait(context.browser, 3).until(
        EC.presence_of_element_located((By.XPATH, Locators.CART_ICON))
    )
    cart_button.click()


@then('the product "{product_name}" is in the cart')
def step_verify_cart(context, product_name):
    """Verify that the product is in the cart"""
    cart_item_xpath = Locators.cart_item(product_name)
    cart_item = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, cart_item_xpath))
    )
    assert cart_item is not None, f"Item '{product_name}' not found in cart"
    # Verify the cart page title
    cart_title = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, Locators.CART_PAGE_TITLE))
    )
    assert cart_title.text == "Your Cart", "Incorrect page title"


@when("the user clicks checkout")
def step_click_checkout(context):
    """Click on the checkout button"""
    checkout_button = context.browser.find_element(
        By.XPATH, Locators.CHECKOUT_BUTTON)
    checkout_button.click()


@then("the checkout page loads")
def step_verify_checkout(context):
    """Verify that the checkout page is displayed"""
    try:
        checkout_info = WebDriverWait(context.browser, 1).until(
            EC.presence_of_element_located((By.XPATH, Locators.CHECKOUT_PAGE))
        )
        assert checkout_info is not None, "Checkout page not found"
    except TimeoutException:
        assert False, "Checkout page not found within the given time"


@when("the user enters their information")
def step_fill_checkout(context):
    """Fill the checkout form"""
    for row in context.table:
        first_name = context.browser.find_element(
            By.XPATH, Locators.FIRST_NAME
        )
        last_name = context.browser.find_element(
            By.XPATH, Locators.LAST_NAME
        )
        postal_code = context.browser.find_element(
            By.XPATH, Locators.POSTAL_CODE
        )

        first_name.send_keys(row["First Name"])
        last_name.send_keys(row["Last Name"])
        postal_code.send_keys(row["Zip/Postal Code"])


@when("the user clicks continue")
def click_continue(context):
    """Click on the continue button"""
    continue_button = context.browser.find_element(
        By.XPATH, Locators.CONTINUE_BUTTON
    )
    continue_button.click()


@then("the checkout overview page loads")
def step_verify_overview(context):
    """Verify that the overview page is displayed"""
    assert (
        "https://www.saucedemo.com/checkout-step-two.html"
        in context.browser.current_url
    ), "Not on the overview page"
    # Verify the overview page title
    overview_title = (
        context.browser.find_element(By.XPATH, Locators.CHECKOUT_OVERVIEW))
    assert overview_title.text == "Checkout: Overview", "Incorrect page title"


@when("the user clicks finish")
def step_click_finish(context):
    """Click on the finish button"""
    finish_button = (
        context.browser.find_element(By.XPATH, Locators.FINISH_BUTTON))
    finish_button.click()


@then("the confirmation page loads")
def step_verify_confirmation(context):
    """Verify that the confirmation page is displayed"""
    assert (
        "https://www.saucedemo.com/checkout-complete.html"
        in context.browser.current_url
    ), "Not on the confirmation page"
    # Verify the confirmation page title
    confirmation_title = context.browser.find_element(
        By.XPATH, Locators.CHECKOUT_COMPLETE
    )
    assert confirmation_title.text == "Checkout: Complete!", \
        "Incorrect page title"
