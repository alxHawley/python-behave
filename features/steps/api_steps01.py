import requests
from behave import given, when, then

from dateutil.parser import parse

import json
import jsonschema


base_url = "https://restful-booker.herokuapp.com/"
ping_endpoint = "ping"
booking_endpoint = "booking/"
auth_endpoint = "auth"

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

# Given steps

# POST to create a booking and get context
@given('a hotel booking is created')
def step_create_booking(context):
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
        
        context.response = requests.post(base_url + booking_endpoint, json={
            "firstname": context.firstname,
            "lastname": context.lastname,
            "totalprice": context.totalprice,
            "depositpaid": context.depositpaid,
            "bookingdates": {
                "checkin": checkin_date,
                "checkout": checkout_date
            },
            "additionalneeds": context.additionalneeds
        }

        # Store the response values for bookingid and booking
        )
        context.bookingid = str(context.response.json()["bookingid"])
        context.booking = context.response.json()

        assert context.response.status_code == 200 # assert that the booking was created successfully

# When steps

# When the booking details are provided from the response
@when('the booking details are provided')
def step_validate_booking(context):
    # Load the JSON schema from the file
    with open("booking_schema.json", "r") as f:
        schema = json.load(f)

    # Validate the stored booking data against the schema
    jsonschema.validate(context.booking, schema)


# Then steps

# Then a booking ID is obtained
@then('a booking ID is obtained')
def step_booking_id_obtained(context):
    assert context.bookingid is not None
