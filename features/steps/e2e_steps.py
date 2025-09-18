"""
E2E steps for 'e2e.feature' using Page Object Model
"""

import logging
from typing import Dict

# pylint: disable=no-name-in-module
from behave import then, when
# pylint: enable=no-name-in-module

from pages.page_factory import PageFactory

logging.basicConfig(level=logging.INFO)


def get_page_factory(context):
    """Get or create PageFactory instance"""
    if not hasattr(context, 'page_factory'):
        context.page_factory = PageFactory(context.browser)
    return context.page_factory


@when('the user adds the product "{product_name}" to the cart')
def step_add_to_cart(context, product_name):
    """Add a product to the cart"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    success = product_page.add_product_to_cart(product_name)
    assert success, f"Failed to add product '{product_name}' to cart"


@when("the user clicks on the cart icon")
def step_click_cart(context):
    """Click on the cart icon"""
    page_factory = get_page_factory(context)
    product_page = page_factory.product_page
    
    success = product_page.click_cart_icon()
    assert success, "Failed to click cart icon or navigate to cart page"


@then('the product "{product_name}" is in the cart')
def step_verify_cart(context, product_name):
    """Verify that the product is in the cart"""
    page_factory = get_page_factory(context)
    cart_page = page_factory.cart_page
    
    success = cart_page.verify_cart_contents(product_name)
    assert success, f"Product '{product_name}' not properly verified in cart"


@when("the user clicks checkout")
def step_click_checkout(context):
    """Click on the checkout button"""
    page_factory = get_page_factory(context)
    cart_page = page_factory.cart_page
    
    success = cart_page.click_checkout_button()
    assert success, "Failed to click checkout button"


@then("the checkout page loads")
def step_verify_checkout(context):
    """Verify that the checkout page is displayed"""
    page_factory = get_page_factory(context)
    checkout_page = page_factory.checkout_page
    
    success = checkout_page.verify_checkout_page()
    assert success, "Checkout page not loaded properly"


@when("the user enters their information")
def step_fill_checkout(context):
    """Fill the checkout form"""
    page_factory = get_page_factory(context)
    checkout_page = page_factory.checkout_page
    
    # Convert table data to dictionary
    checkout_data = {}
    for row in context.table:
        checkout_data = {
            "First Name": row["First Name"],
            "Last Name": row["Last Name"],
            "Zip/Postal Code": row["Zip/Postal Code"]
        }
        break  # Take first row if multiple
    
    success = checkout_page.fill_checkout_form(checkout_data)
    assert success, "Failed to fill checkout form"


@when("the user clicks continue")
def click_continue(context):
    """Click on the continue button"""
    page_factory = get_page_factory(context)
    checkout_page = page_factory.checkout_page
    
    success = checkout_page.click_continue_button()
    assert success, "Failed to click continue button"


@then("the checkout overview page loads")
def step_verify_overview(context):
    """Verify that the overview page is displayed"""
    page_factory = get_page_factory(context)
    checkout_overview_page = page_factory.checkout_overview_page
    
    success = checkout_overview_page.verify_overview_page()
    assert success, "Checkout overview page not loaded properly"


@when("the user clicks finish")
def step_click_finish(context):
    """Click on the finish button"""
    page_factory = get_page_factory(context)
    checkout_overview_page = page_factory.checkout_overview_page
    
    success = checkout_overview_page.click_finish_button()
    assert success, "Failed to click finish button"


@then("the confirmation page loads")
def step_verify_confirmation(context):
    """Verify that the confirmation page is displayed"""
    page_factory = get_page_factory(context)
    checkout_complete_page = page_factory.checkout_complete_page
    
    success = checkout_complete_page.verify_complete_page()
    assert success, "Checkout complete page not loaded properly"
