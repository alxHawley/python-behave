"""
Step definitions for 'api.feature' - Hotel Booking Management
"""

import os
import json

import jsonschema
import requests

# pylint: disable=no-name-in-module
from behave import given, then, when

# pylint: enable=no-name-in-module
from dateutil.parser import parse

from utils.schema_loader import load_schema

BASE_URL = os.getenv("BASE_URL", "http://localhost:3001/")
BOOKING_ENDPOINT = "booking"
AUTH_ENDPOINT = "auth"

# headers for unauthenticated requests (POST, GET)
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# headers for authenticated requests (PUT, PATCH, DELETE)
headers_with_cookie = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Cookie": "",
}


# ============================================================================
# GIVEN STEPS - Setup and Context
# ============================================================================

@given("I have valid booking credentials")
def step_have_valid_credentials(context):
    """Setup valid authentication credentials for booking operations"""
    context.username = "admin"
    context.password = "password123"
    context.token = None


@given("I have a new hotel booking with the following details")
def step_have_booking_details(context):
    """Store booking details from data table for later use"""
    booking_data = context.table[0]  # Get first row from table
    context.booking_details = {
        "firstname": booking_data["firstname"],
        "lastname": booking_data["lastname"],
        "totalprice": int(booking_data["totalprice"]),
        "depositpaid": booking_data["depositpaid"].lower() == "true",
        "checkin": booking_data["checkin"],
        "checkout": booking_data["checkout"],
        "additionalneeds": booking_data["additionalneeds"] if booking_data["additionalneeds"] != "None" else None
    }


@given("a booking has been created")
def step_booking_exists(context):
    """Ensure a booking exists by creating one if it doesn't"""
    if not hasattr(context, 'bookingid') or context.bookingid is None:
        # Create a booking if one doesn't exist
        step_create_booking_internal(context)


@given("I have updated booking details")
def step_have_updated_details(context):
    """Store updated booking details from data table"""
    booking_data = context.table[0]
    context.updated_details = {
        "firstname": booking_data["firstname"],
        "lastname": booking_data["lastname"],
        "totalprice": int(booking_data["totalprice"]),
        "depositpaid": booking_data["depositpaid"].lower() == "true",
        "checkin": booking_data["checkin"],
        "checkout": booking_data["checkout"],
        "additionalneeds": booking_data["additionalneeds"] if booking_data["additionalneeds"] != "None" else None
    }


@given("I want to update specific booking details")
def step_have_partial_update_details(context):
    """Store partial update details from data table"""
    booking_data = context.table[0]
    context.partial_update = {}
    
    if "totalprice" in booking_data:
        context.partial_update["totalprice"] = int(booking_data["totalprice"])
    if "depositpaid" in booking_data:
        context.partial_update["depositpaid"] = booking_data["depositpaid"].lower() == "true"
    if "checkin" in booking_data:
        if "bookingdates" not in context.partial_update:
            context.partial_update["bookingdates"] = {}
        context.partial_update["bookingdates"]["checkin"] = booking_data["checkin"]
    if "checkout" in booking_data:
        if "bookingdates" not in context.partial_update:
            context.partial_update["bookingdates"] = {}
        context.partial_update["bookingdates"]["checkout"] = booking_data["checkout"]


@given("I have an invalid booking reference")
def step_have_invalid_booking_id(context):
    """Set an invalid booking ID for error testing"""
    context.bookingid = "99999"  # Non-existent booking ID


@given("I do not have valid authorization")
def step_no_authorization(context):
    """Remove authorization for error testing"""
    context.token = None


# ============================================================================
# WHEN STEPS - Actions
# ============================================================================

@when("I create the booking")
def step_create_booking(context):
    """Create a new hotel booking"""
    step_create_booking_internal(context)


@when("I request the booking details")
def step_request_booking_details(context):
    """Retrieve booking details by ID"""
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    context.response = requests.get(url, headers=headers, timeout=5)
    if context.response.status_code == 200:
        context.booking = context.response.json()


@when("I update the booking")
def step_update_booking(context):
    """Update booking with complete information"""
    # Get authentication token first
    if not context.token:
        step_get_auth_token(context)
    
    headers_with_cookie["Cookie"] = f"token={context.token}"
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    
    # Use updated details from context
    update_data = context.updated_details.copy()
    update_data["bookingdates"] = {
        "checkin": update_data.pop("checkin"),
        "checkout": update_data.pop("checkout")
    }
    
    context.response = requests.put(
        url,
        headers=headers_with_cookie,
        json=update_data,
        timeout=5,
    )


@when("I partially update the booking")
def step_partial_update_booking(context):
    """Partially update booking information"""
    # Get authentication token first
    if not context.token:
        step_get_auth_token(context)
    
    headers_with_cookie["Cookie"] = f"token={context.token}"
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    
    context.response = requests.patch(
        url,
        headers=headers_with_cookie,
        json=context.partial_update,
        timeout=5,
    )


@when("I cancel the booking")
def step_cancel_booking(context):
    """Cancel/delete a hotel booking"""
    # Get authentication token first
    if not context.token:
        step_get_auth_token(context)
    
    headers_with_cookie["Cookie"] = f"token={context.token}"
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    context.response = requests.delete(
        url, headers=headers_with_cookie, timeout=5
    )


@when("I attempt to update the booking")
def step_attempt_update_booking(context):
    """Attempt to update booking without proper authorization"""
    # Use invalid or no token
    headers_with_cookie["Cookie"] = f"token={context.token or 'invalid'}"
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    
    update_data = context.updated_details.copy()
    update_data["bookingdates"] = {
        "checkin": update_data.pop("checkin"),
        "checkout": update_data.pop("checkout")
    }
    
    context.response = requests.put(
        url,
        headers=headers_with_cookie,
        json=update_data,
        timeout=5,
    )


# ============================================================================
# THEN STEPS - Assertions and Validations
# ============================================================================

@then("the booking should be created successfully")
def step_booking_created_successfully(context):
    """Verify that the booking was created successfully"""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}: {context.response.text}"
    assert context.bookingid is not None, "Booking ID should be generated"


@then("I should receive a booking confirmation")
def step_receive_booking_confirmation(context):
    """Verify that a booking confirmation is received"""
    response_data = context.response.json()
    assert "bookingid" in response_data, "Booking confirmation should include booking ID"
    assert "booking" in response_data, "Booking confirmation should include booking details"


@then("I should receive the correct booking information")
def step_receive_correct_booking_info(context):
    """Verify that correct booking information is returned"""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"
    assert context.booking is not None, "Booking details should be returned"


@then("the booking data should be valid")
def step_booking_data_valid(context):
    """Verify that booking data is valid according to schema"""
    assert context.response.status_code == 200
    
    # Load and validate against schema
    schema = load_schema("booking_schema.json")
    jsonschema.validate(context.response.json(), schema)


@then("the booking should be updated successfully")
def step_booking_updated_successfully(context):
    """Verify that the booking was updated successfully"""
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}: {context.response.text}"


@then("I should receive the updated booking details")
def step_receive_updated_booking_details(context):
    """Verify that updated booking details are returned"""
    assert context.response.status_code == 200
    response_data = context.response.json()
    
    # Verify the response contains booking data
    assert "firstname" in response_data, "Updated booking should include firstname"
    assert "lastname" in response_data, "Updated booking should include lastname"
    assert "totalprice" in response_data, "Updated booking should include totalprice"


@then("the booking should be cancelled successfully")
def step_booking_cancelled_successfully(context):
    """Verify that the booking was cancelled successfully"""
    assert context.response.status_code == 201, f"Expected 201, got {context.response.status_code}: {context.response.text}"


@then("the booking should no longer be accessible")
def step_booking_no_longer_accessible(context):
    """Verify that the cancelled booking is no longer accessible"""
    # Try to retrieve the cancelled booking
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    response = requests.get(url, headers=headers, timeout=5)
    assert response.status_code == 404, "Cancelled booking should return 404"


@then("I should receive a not found error")
def step_receive_not_found_error(context):
    """Verify that a not found error is returned"""
    assert context.response.status_code == 404, f"Expected 404, got {context.response.status_code}"


@then("I should receive an unauthorized error")
def step_receive_unauthorized_error(context):
    """Verify that an unauthorized error is returned"""
    assert context.response.status_code == 403, f"Expected 403, got {context.response.status_code}"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def step_create_booking_internal(context):
    """Internal helper function to create a booking"""
    # Get authentication token first
    step_get_auth_token(context)
    
    # Prepare booking data
    booking_data = context.booking_details.copy()
    booking_data["bookingdates"] = {
        "checkin": booking_data.pop("checkin"),
        "checkout": booking_data.pop("checkout")
    }
    
    # Create the booking
    url = f"{BASE_URL}{BOOKING_ENDPOINT}"
    context.response = requests.post(
        url,
        headers=headers,
        json=booking_data,
        timeout=5,
    )
    
    # Store response data
    if context.response.status_code == 200:
        response_data = context.response.json()
        context.bookingid = str(response_data["bookingid"])
        context.booking = response_data["booking"]


def step_get_auth_token(context):
    """Helper function to get authentication token"""
    auth_response = requests.post(
        f"{BASE_URL}{AUTH_ENDPOINT}",
        headers=headers,
        json={"username": context.username, "password": context.password},
        timeout=5,
    )
    
    if auth_response.status_code == 200:
        context.token = auth_response.json()["token"]
        assert context.token != "", "Authentication token should not be empty"
    else:
        raise AssertionError(f"Authentication failed: {auth_response.status_code} - {auth_response.text}")
