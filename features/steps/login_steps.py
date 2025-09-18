"""
Selenium steps for 'login.feature' using Page Object Model
"""

import logging
from time import time
from typing import Optional

# pylint: disable=no-name-in-module
from behave import given, then, when
# pylint: enable=no-name-in-module

from pages.page_factory import PageFactory

logging.basicConfig(level=logging.INFO)

# Constants
DEFAULT_WAIT_TIME = 10
PERFORMANCE_WAIT_TIME = 5
ERROR_WAIT_TIME = 3


def get_page_factory(context):
    """Get or create PageFactory instance"""
    if not hasattr(context, 'page_factory'):
        context.page_factory = PageFactory(context.browser)
    return context.page_factory


@given("a user is on the login page")
def step_login_page(context):
    """Navigate to the login page and verify it's loaded"""
    page_factory = get_page_factory(context)
    login_page = page_factory.login_page
    
    login_page.navigate_to_login_page()
    assert login_page.is_login_page_loaded(), "Login page not loaded properly"


@given('the user enters "{username}" and "{password}"')
@when('the user enters "{username}" and "{password}"')
def step_enter_credentials(context, username, password):
    """Enter the username and password and click the login button"""
    page_factory = get_page_factory(context)
    login_page = page_factory.login_page
    
    # Start timing for performance tests
    context.start_time = time()
    
    # Perform login
    success = login_page.login(username, password)
    assert success, "Failed to enter credentials or click login button"


@when('the user enters "" and ""')
def step_enter_empty_credentials(context):
    """Enter empty username and password and click the login button"""
    step_enter_credentials(context, "", "")


@when('the user enters "" and "secret_sauce"')
def step_enter_empty_username(context):
    """Enter empty username and password, then click the login button"""
    step_enter_credentials(context, "", "secret_sauce")


@when('the user enters "standard_user" and ""')
def step_enter_empty_password(context):
    """Enter username and empty password, then click the login button"""
    step_enter_credentials(context, "standard_user", "")


@given('the user is logged in with "{username}" and "{password}"')
def step_user_logged_in(context, username, password):
    """Log in the user with provided credentials"""
    step_enter_credentials(context, username, password)
    step_login_success(context)


@when("the user opens the navigation menu")
def step_open_menu(context):
    """Open the navigation menu"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    success = product_page.open_navigation_menu()
    assert success, "Failed to open navigation menu"


@then("the user should be successfully logged in")
def step_login_success(context):
    """Verify that the user is successfully logged in and is on the product page"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    # Check if login was successful
    assert product_page.is_product_page_loaded(), "Login failed - not on product page"
    assert product_page.is_correct_page_title(), "Incorrect page title"


@then("the user should not be able to login")
def step_user_not_able_to_login(context):
    """Verify that the user is not able to login by checking for error container"""
    page_factory = get_page_factory(context)
    login_page = page_factory.login_page
    
    # Wait a moment for error to appear
    import time
    time.sleep(1)
    
    assert login_page.is_error_message_displayed(), "Error message not displayed - login should have failed"


@then('the user should see an error message "{message}"')
def step_error_message(context, message):
    """Verify that the user sees the correct error message"""
    page_factory = get_page_factory(context)
    login_page = page_factory.login_page
    
    # Wait for error message to appear
    import time
    time.sleep(1)
    
    actual_message = login_page.get_error_message()
    assert actual_message is not None, f"Error message not found for: {message}"
    assert actual_message == message, f"Expected '{message}' but got '{actual_message}'"


@then('the user should be "<expected_result>"')
def step_user_should_be(context, expected_result):
    """Handle different expected results for data-driven tests"""
    if expected_result == "successfully logged in":
        step_login_success(context)
    elif expected_result == "not able to login":
        step_user_not_able_to_login(context)
    else:
        raise ValueError(f"Unknown expected result: {expected_result}")


@then('the user should see "<error_message>"')
def step_user_should_see_error(context, error_message):
    """Handle error messages for data-driven tests"""
    if error_message and error_message.strip():
        step_error_message(context, error_message)


# Additional step definitions for data-driven tests
@then('the user should be "successfully logged in"')
def step_user_should_be_successfully_logged_in(context):
    """Handle successful login for data-driven tests"""
    step_login_success(context)


@then('the user should be "not able to login"')
def step_user_should_be_not_able_to_login(context):
    """Handle failed login for data-driven tests"""
    step_user_not_able_to_login(context)


@then('the user should see ""')
def step_user_should_see_empty_error(context):
    """Handle empty error message for data-driven tests (successful login)"""
    # For successful logins, we don't expect any error message
    pass


@then('the user should see "Epic sadface: Sorry, this user has been locked out."')
def step_user_should_see_locked_out_error(context):
    """Handle locked out user error message for data-driven tests"""
    step_error_message(context, "Epic sadface: Sorry, this user has been locked out.")


@then("the user is able to login")
def step_user_is_able_to_login(context):
    """Verify that the user is able to login (used in e2e background)"""
    step_login_success(context)


@when("the user clicks on the logout button")
def step_logout(context):
    """Click on the logout button"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    success = product_page.click_logout()
    assert success, "Failed to click logout button"


@then("the user should be logged out")
def step_logout_success(context):
    """Verify that the user is logged out and redirected to login page"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    assert product_page.is_logged_out(), "Logout failed - not redirected to login page"


@then("the user should be redirected to the login page")
def step_redirected_to_login(context):
    """Verify that the user is redirected to the login page"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    assert product_page.is_logged_out(), "Not redirected to login page"


@then("the product page should be displayed")
def step_product_page_displayed(context):
    """Verify that the product page is displayed"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    assert product_page.is_product_page_loaded(), "Product page not displayed"
    assert product_page.is_correct_page_title(), "Incorrect page title"


@then("the product page should load in less than 1 second")
def step_page_load_performance(context):
    """Verify that the product page loads in less than 1 second"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    # Wait for the inventory page to load completely
    success = product_page.wait_for_page_load(PERFORMANCE_WAIT_TIME)
    assert success, "Product page did not load completely"
    
    # Calculate the time it took for the page to load
    end_time = time()
    load_time = end_time - context.start_time
    logging.info("Page load took %.3f seconds", load_time)
    
    assert load_time < 1.0, f"Performance test failed: Page loaded in {load_time:.3f}s, expected < 1.0s"


@then("the product page should load in less than 3 seconds")
def step_page_load_performance_glitch(context):
    """Verify that the product page loads in less than 3 seconds (for glitch user)"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    # Wait for the inventory page to load completely
    success = product_page.wait_for_page_load(PERFORMANCE_WAIT_TIME)
    assert success, "Product page did not load completely"
    
    # Calculate the time it took for the page to load
    end_time = time()
    load_time = end_time - context.start_time
    logging.info("Page load took %.3f seconds", load_time)
    
    assert load_time < 3.0, f"Performance test failed: Page loaded in {load_time:.3f}s, expected < 3.0s"
