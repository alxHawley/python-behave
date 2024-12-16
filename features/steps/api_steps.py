"""
Step definitions for 'api.feature'
"""

import logging
import os

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


@given("a hotel booking is created")
def step_create_booking(context):
    """
    Create a booking and store the booking ID and booking data in the context
    """
    for booking_data in context.table:  # extract the data table
        context.firstname = booking_data["firstname"]
        context.lastname = booking_data["lastname"]
        context.totalprice = int(booking_data["totalprice"])  # to integer
        context.depositpaid = bool(booking_data["depositpaid"])  # to boolean
        context.checkin = booking_data["checkin"]
        context.checkout = booking_data["checkout"]
        context.additionalneeds = booking_data["additionalneeds"]
        checkin_date = parse(context.checkin).strftime("%Y-%m-%d")  # to date
        checkout_date = parse(context.checkout).strftime("%Y-%m-%d")

        url = BASE_URL + BOOKING_ENDPOINT
        logging.info(f"POST request URL: {url}")

        context.response = requests.post(
            url,
            headers=headers,
            json={
                "firstname": context.firstname,
                "lastname": context.lastname,
                "totalprice": context.totalprice,
                "depositpaid": context.depositpaid,
                "bookingdates": {
                    "checkin": checkin_date,
                    "checkout": checkout_date,
                },
                "additionalneeds": context.additionalneeds,
            },
            timeout=5,
        )
        logging.info(f"Response status code: {context.response.status_code}")
        logging.info(f"Response body: {context.response.json()}")

        # Store the response values for bookingid and booking
        context.bookingid = str(context.response.json()["bookingid"])
        context.booking = context.response.json()["booking"]
        # assert that the booking was created successfully
        assert context.response.status_code == 200


@when("the booking details are provided")
def step_validate_booking(context):
    """Validate the booking details against the schema"""
    # Load the JSON schema from the file
    schema = load_schema("booking_id_schema.json")
    # Validate the entire response context against the schema
    jsonschema.validate(context.response.json(), schema)


@when("a GET request is made with the booking ID")
def step_get_booking(context):
    """Get the booking details using the booking ID"""
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    logging.info(f"GET request URL: {url}")
    context.response = requests.get(url, headers=headers, timeout=5)
    context.booking = context.response.json()


@when("a PUT request is made with the booking ID")
def step_update_booking(context):
    """Update the booking details using the booking ID"""
    headers_with_cookie["Cookie"] = f"token={context.token}"  # auth token
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    logging.info(f"PUT request URL: {url}")
    context.response = requests.put(
        url,
        headers=headers_with_cookie,
        json={
            "firstname": context.firstname,
            "lastname": context.lastname,
            "totalprice": context.totalprice,
            "depositpaid": context.depositpaid,
            "bookingdates": {
                "checkin": context.checkin,
                "checkout": context.checkout,
            },
            "additionalneeds": context.additionalneeds,
        },
        timeout=5,
    )
    logging.info(f"Response status code: {context.response.status_code}")
    logging.info(f"Response body: {context.response.json()}")


@when("a PATCH request is made with the booking ID")
def step_partial_update_booking(context):
    """Partially update the booking details using the booking ID"""
    # Extract the booking ID and new booking details from the table
    new_booking = context.table[0]

    # Construct the PATCH request data
    data = {}
    if "totalprice" in new_booking:
        data["totalprice"] = int(new_booking["totalprice"])
    if "depositpaid" in new_booking:
        data["depositpaid"] = new_booking["depositpaid"] == "true"
    if "checkin" in new_booking:
        data["bookingdates"] = {"checkin": new_booking["checkin"]}
    if "checkout" in new_booking:
        if "bookingdates" not in data:
            data["bookingdates"] = {}
        data["bookingdates"]["checkout"] = new_booking["checkout"]

    # Send the PATCH request and store the response
    headers_with_cookie["Cookie"] = f"token={context.token}"  # auth token
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    logging.info(f"PATCH request URL: {url}")

    response = requests.patch(
        url,
        headers=headers_with_cookie,
        json=data,
        timeout=5,
    )
    context.response = response
    logging.info(f"Response status code: {context.response.status_code}")
    logging.info(f"Response body: {context.response.json()}")

    # Update the context.booking dictionary with the new booking data
    context.booking.update(response.json())

    # Assign the new_booking variable to the new booking data
    context.new_booking = response.json()


@when("a DELETE request is made with the booking ID")
def step_delete_booking(context):
    """Delete the booking using the booking ID"""
    headers_with_cookie["Cookie"] = (
        f"token={context.token}"  # add the token to the headers
    )
    url = f"{BASE_URL}{BOOKING_ENDPOINT}/{context.bookingid}"
    logging.info(f"DELETE request URL: {url}")
    context.response = requests.delete(
        url, headers=headers_with_cookie, timeout=5
    )
    logging.info(f"Response status code: {context.response.status_code}")


@then("a booking ID is obtained")
def step_booking_id_obtained(context):
    """Verify that a booking ID is obtained"""
    assert context.bookingid is not None


@then("an auth token is obtained")
def step_auth_token_obtained(context):
    """Verify that an auth token is obtained"""
    context.response = requests.post(
        BASE_URL + AUTH_ENDPOINT,
        headers=headers,
        json={"username": "admin", "password": "password123"},
        timeout=5,
    )
    context.token = context.response.json()["token"]
    # assert that the token is not empty
    assert context.token != ""
    assert context.response.status_code == 200


@then("the booking details are retrieved successfully")
def step_booking_details_retrieved(context):
    """Verify that the booking details are retrieved successfully"""
    assert context.response.status_code == 200

    # Load the JSON schema from the file
    schema = load_schema("booking_schema.json")

    # Validate the entire response context against the schema
    jsonschema.validate(context.response.json(), schema)


@then("the booking details are updated successfully")
def step_booking_details_updated(context):
    """Verify that the booking details are updated successfully"""
    assert context.response.status_code == 200

    # Log the entire JSON response for debugging
    response_json = context.response.json()
    logging.info(f"Response JSON: {response_json}")

    # assert that booking data returned matches data used to update the booking
    assert response_json["firstname"] == context.booking["firstname"]
    assert response_json["lastname"] == context.booking["lastname"]
    assert response_json["totalprice"] == context.booking["totalprice"]
    assert response_json["depositpaid"] == context.booking["depositpaid"]
    assert (
        response_json["bookingdates"]["checkin"]
        == context.booking["bookingdates"]["checkin"]
    )
    assert (
        response_json["bookingdates"]["checkout"]
        == context.booking["bookingdates"]["checkout"]
    )


@then("the booking details are partially updated successfully")
def step_booking_details_partially_updated(context):
    """Verify that the booking details are partially updated successfully"""
    assert context.response.status_code == 200

    # Log the entire JSON response for debugging
    response_json = context.response.json()
    logging.info(f"Response JSON: {response_json}")

    # Log the expected and actual values for debugging
    logging.info(f"Expected depositpaid: {context.booking['depositpaid']}")
    logging.info(f"Actual depositpaid: {response_json['depositpaid']}")

    # assert that booking data returned matches data used to update booking
    assert response_json["firstname"] == context.booking["firstname"]
    assert response_json["lastname"] == context.booking["lastname"]
    assert response_json["totalprice"] == context.booking["totalprice"]
    assert response_json["depositpaid"] == context.booking["depositpaid"]
    assert (
        response_json["bookingdates"]["checkin"]
        == context.booking["bookingdates"]["checkin"]
    )
    assert (
        response_json["bookingdates"]["checkout"]
        == context.booking["bookingdates"]["checkout"]
    )


@then("the booking is deleted successfully")
def step_booking_deleted(context):
    """Verify that the booking is 'deleted' successfully"""
    assert context.response.status_code == 201
    assert (
        context.response.text == "Created"
    )  # the API does not respond with expected "Deleted"
