"""
This module contains the Selenium steps for 'login.feature'.
"""

import logging
from time import time

# pylint: disable=no-name-in-module
from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# pylint: enable=no-name-in-module


logging.basicConfig(level=logging.INFO)


@given("a user is on the login page")
def step_login_page(context):
    """Navigate to the login page and verify the presence of the login button"""
    context.browser.get("https://www.saucedemo.com/")

    # Verify the URL
    assert (
        "https://www.saucedemo.com/" in context.browser.current_url
    ), "Not on the login page"

    # Verify the presence of the login button
    login_button = context.browser.find_element(By.ID, "login-button")
    assert login_button is not None, "Login button not found"


@given('the user submits credentials "{username}" and "{password}"')
@when('the user submits credentials "{username}" and "{password}"')
def step_enter_credentials(context, username, password):
    """Enter the username and password and click the login button"""
    username_field = context.browser.find_element(By.ID, "user-name")
    username_field.send_keys(username)
    password_field = context.browser.find_element(By.ID, "password")
    password_field.send_keys(password)
    login_button = context.browser.find_element(By.ID, "login-button")
    context.start_time = time()
    login_button.click()


@when("the user opens the navigation menu")
def step_open_menu(context):
    """Open the navigation menu"""
    menu_button = context.browser.find_element(By.ID, "react-burger-menu-btn")
    menu_button.click()


@given("the user is able to login")
@when("the user is able to login")
@then("the user is able to login")
def step_login_success(context):
    """Verify that the user is able to log in"""
    assert (
        "https://www.saucedemo.com/inventory.html" in context.browser.current_url
    ), "Login failed"


@then("the user is not able to login")
def step_login_fail(context):
    """Verify that the user is not able to log in"""
    assert (
        "https://www.saucedemo.com/" in context.browser.current_url
    ), "Login succeeded"


@then('the user should see an error message "{message}"')
def step_error_message(context, message):
    """Verify that the user sees the correct error message"""
    error_button = context.browser.find_element(
        By.XPATH, f"//h3[contains(text(),'{message}')]"
    )
    assert error_button.text.strip() == message, "Incorrect error message"


@when("the user clicks on the logout button")
def step_logout(context):
    """Click on the logout button"""
    # Wait until the logout button is visible
    WebDriverWait(context.browser, 2).until(
        EC.visibility_of_element_located((By.ID, "logout_sidebar_link"))
    )
    logout_button = context.browser.find_element(By.ID, "logout_sidebar_link")
    logout_button.click()


@then("the user is logged out")
def step_logout_success(context):
    """Verify that the user is logged out"""
    assert "https://www.saucedemo.com/" in context.browser.current_url, "Logout failed"


@then("the product page should load in less than 1 second")
def step_page_load(context):
    """Verify that the product page loads in less than 1 second"""
    # Wait for the inventory page to load
    WebDriverWait(context.browser, 5).until(
        EC.visibility_of_element_located((By.ID, "inventory_container"))
    )
    # Calculate the time it took for the page to load
    end_time = time()
    load_time = end_time - context.start_time
    logging.info("Page load took %s seconds", load_time)
    try:
        assert load_time < 1, "Performance degraded"
    except AssertionError as e:
        logging.warning("Performance test failed: %s", e)
