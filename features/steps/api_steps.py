"""
This module contains step definitions for 'api.feature'.
"""

import requests
# pylint: disable=no-name-in-module
from behave import given, when, then
# pylint: enable=no-name-in-module
from dateutil.parser import parse
import jsonschema
from utils.schema_loader import load_schema


BASE_URL = "https://restful-booker.herokuapp.com/"
BOOKING_ENDPOINT = "booking/"
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
    "Cookie": ""
}

@given('a hotel booking is created')
def step_create_booking(context):
    """Create a booking and store the booking ID and booking data in the context"""
    for booking_data in context.table:  # extract the data table
        context.firstname = booking_data['firstname']
        context.lastname = booking_data['lastname']
        context.totalprice = int(booking_data['totalprice'])  # convert to integer
        context.depositpaid = bool(booking_data['depositpaid'])  # convert to boolean
        context.checkin = booking_data['checkin']
        context.checkout = booking_data['checkout']
        context.additionalneeds = booking_data['additionalneeds']
        checkin_date = parse(context.checkin).strftime('%Y-%m-%d')  # convert to date format
        checkout_date = parse(context.checkout).strftime('%Y-%m-%d')

        context.response = requests.post(BASE_URL + BOOKING_ENDPOINT, headers=headers, json={
            "firstname": context.firstname,
            "lastname": context.lastname,
            "totalprice": context.totalprice,
            "depositpaid": context.depositpaid,
            "bookingdates": {
                "checkin": checkin_date,
                "checkout": checkout_date
            },
            "additionalneeds": context.additionalneeds
        }, timeout=5)
        # Store the response values for bookingid and booking
        context.bookingid = str(context.response.json()["bookingid"])
        context.booking = context.response.json()
        # assert that the booking was created successfully
        assert context.response.status_code == 200  


@when('the booking details are provided')
def step_validate_booking(context):
    """Validate the booking details against the schema"""
    # Load the JSON schema from the file
    schema = load_schema("booking_id_schema.json")
    # Validate the entire response context against the schema
    jsonschema.validate(context.response.json(), schema)


@when('a GET request is made with the booking ID')
def step_get_booking(context):
    """Get the booking details using the booking ID"""
    context.response = requests.get(BASE_URL + BOOKING_ENDPOINT + context.bookingid,
                                    headers=headers, timeout=5)
    context.booking = context.response.json()


@when('a PUT request is made with the booking ID')
def step_update_booking(context):
    """Update the booking details using the booking ID"""
    for booking_data in context.table:
        # Extract the booking data from the table
        firstname = booking_data['firstname']
        lastname = booking_data['lastname']
        totalprice = int(booking_data['totalprice'])
        depositpaid = bool(booking_data['depositpaid'])
        checkin = booking_data['checkin']
        checkout = booking_data['checkout']
        additionalneeds = booking_data['additionalneeds']

        # Convert the checkin and checkout dates to the correct format
        checkin_date = parse(checkin).strftime('%Y-%m-%d')
        checkout_date = parse(checkout).strftime('%Y-%m-%d')

        # Construct the request body
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "totalprice": totalprice,
            "depositpaid": depositpaid,
            "bookingdates": {
                "checkin": checkin_date,
                "checkout": checkout_date
            },
            "additionalneeds": additionalneeds
        }

        # Send the PUT request and store the response
        headers_with_cookie["Cookie"] = f"token={context.token}"  # add the token to the headers
        response = requests.put(BASE_URL + BOOKING_ENDPOINT + context.bookingid,
                                headers=headers_with_cookie, json=data, timeout=5)
        context.response = response

        # Update the context.booking dictionary with the new booking data
        context.booking.update(response.json())


@when('a PATCH request is made with the booking ID')
def step_partial_update_booking(context):
    """Partially update the booking details using the booking ID"""
    # Extract the booking ID and new booking details from the table
    booking_id = context.bookingid
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
    headers_with_cookie["Cookie"] = f"token={context.token}"  # add the token to the headers
    response = requests.patch(BASE_URL + BOOKING_ENDPOINT + booking_id,
                              headers=headers_with_cookie, json=data, timeout=5)
    context.response = response

    # Update the context.booking dictionary with the new booking data
    context.booking.update(response.json())

    # Assign the new_booking variable to the new booking data
    context.new_booking = new_booking


@when('a DELETE request is made with the booking ID')
def step_delete_booking(context):
    """Delete the booking using the booking ID"""
    headers_with_cookie["Cookie"] = f"token={context.token}"  # add the token to the headers
    context.response = requests.delete(BASE_URL + BOOKING_ENDPOINT + context.bookingid,
                                       headers=headers_with_cookie, timeout=5)


@then('a booking ID is obtained')
def step_booking_id_obtained(context):
    """Verify that a booking ID is obtained"""
    assert context.bookingid is not None


@then('an auth token is obtained')
def step_auth_token_obtained(context):
    """Verify that an auth token is obtained"""
    context.response = requests.post(BASE_URL + AUTH_ENDPOINT, headers=headers, json={
        "username": "admin",
        "password": "password123"
    }, timeout=5)
    context.token = context.response.json()["token"]
    # assert that the token is not empty
    assert context.token != ""
    assert context.response.status_code == 200

@then('the booking details are retrieved successfully')
def step_booking_details_retrieved(context):
    """Verify that the booking details are retrieved successfully"""
    assert context.response.status_code == 200

    # Load the JSON schema from the file
    schema = load_schema("booking_schema.json")

    # Validate the entire response context against the schema
    jsonschema.validate(context.response.json(), schema)

@then('the booking details are updated successfully')
def step_booking_details_updated(context):
    """Verify that the booking details are updated successfully"""
    assert context.response.status_code == 200

    # assert that the booking data returned matches the data used to update the booking
    assert context.response.json()["firstname"] == context.booking["firstname"]
    assert context.response.json()["lastname"] == context.booking["lastname"]
    assert context.response.json()["totalprice"] == context.booking["totalprice"]
    assert context.response.json()["depositpaid"] == context.booking["depositpaid"]
    assert context.response.json()["bookingdates"]["checkin"] == context.booking["bookingdates"]["checkin"]
    assert context.response.json()["bookingdates"]["checkout"] == context.booking["bookingdates"]["checkout"]
    assert context.response.json()["additionalneeds"] == context.booking["additionalneeds"]


@then('the booking details are partially updated successfully')
def step_booking_details_partially_updated(context):
    """Verify that the booking details are partially updated successfully"""
    assert context.response.status_code == 200
    # Assert that the updated booking data matches the data used to update the booking
    if "totalprice" in context.new_booking:
        assert context.response.json()["totalprice"] == int(context.new_booking["totalprice"])
    if "depositpaid" in context.new_booking:
        assert context.response.json()["depositpaid"] == (context.new_booking["depositpaid"] == "true")
    if "checkin" in context.new_booking:
        assert context.response.json()["bookingdates"]["checkin"] == context.new_booking["checkin"]
    if "checkout" in context.new_booking:
        assert context.response.json()["bookingdates"]["checkout"] == context.new_booking["checkout"]

    # Assert that the original booking data is unchanged
    assert context.response.json()["firstname"] == context.booking["firstname"]
    assert context.response.json()["lastname"] == context.booking["lastname"]
    assert context.response.json()["additionalneeds"] == context.booking["additionalneeds"]


@then('the booking is deleted successfully')
def step_booking_deleted(context):
    """Verify that the booking is 'deleted' successfully"""
    assert context.response.status_code == 201
    assert context.response.text == "Created"  # the API does not respond with expected "Deleted"!
