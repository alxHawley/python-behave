import requests
from behave import given, when, then
from dateutil.parser import parse


base_url = "https://restful-booker.herokuapp.com/"
# auth_endpoint = "auth" # Not used
# booking_endpoint = "booking" # Not used
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


@given('the Restful Booker API is available and returns a {status_code:d} status code for the authentication endpoint')
def step_api_available(context, status_code):
    credentials = {
        "username": "admin",
        "password": "password123"
    }
    context.response = requests.post(base_url + 'auth', headers=headers, json=credentials)
    assert context.response.status_code == status_code
    assert ("reason" not in context.response.json() and "token" in context.response.json()
            and isinstance(context.response.json()["token"], str))


@when('I create the following bookings')
def step_create_bookings(context):
    for booking_data in context.table: # extract the data table
        firstname = booking_data['firstname']
        lastname = booking_data['lastname']
        totalprice = int(booking_data['totalprice'])  # Convert to integer
        depositpaid = bool(booking_data['depositpaid'])  # Convert to boolean
        checkin = booking_data['checkin']
        checkout = booking_data['checkout']
        additionalneeds = booking_data['additionalneeds']
        
        checkin_date = parse(checkin).strftime('%Y-%m-%d')
        checkout_date = parse(checkout).strftime('%Y-%m-%d')
        
        context.response = requests.post(base_url + 'booking', json={
            "firstname": firstname,
            "lastname": lastname,
            "totalprice": totalprice,
            "depositpaid": depositpaid,
            "bookingdates": {
                "checkin": checkin_date,
                "checkout": checkout_date
            },
            "additionalneeds": additionalneeds
        })


@then('the response should have a {status_code:d} status code')
def step_response_status_code(context, status_code):
    assert context.response.status_code == status_code


@then('the response should have the following details')
def step_response_confirmation(context):
    for booking_data in context.table:
        firstname = booking_data['firstname']
        lastname = booking_data['lastname']
        totalprice = int(booking_data['totalprice'])
        depositpaid = bool(booking_data['depositpaid'])
        checkin = booking_data['checkin']
        checkout = booking_data['checkout']
        additionalneeds = booking_data['additionalneeds']
        bookingid = int(booking_data['bookingid'])

        checkin_date = parse(checkin).strftime('%Y-%m-%d')
        checkout_date = parse(checkout).strftime('%Y-%m-%d')

        assert context.response.json()["firstname"] == firstname
        assert context.response.json()["lastname"] == lastname
        assert context.response.json()["totalprice"] == totalprice
        assert context.response.json()["depositpaid"] == depositpaid
        assert context.response.json()["bookingdates"]["checkin"] == checkin_date
        assert context.response.json()["bookingdates"]["checkout"] == checkout_date
        assert context.response.json()["additionalneeds"] == additionalneeds
        assert context.response.json()["bookingid"] == bookingid

        # Log all the values used in the assertions (not working)
        # print("---------------------------------------------------")
        # print("firstname: " + firstname)
        # print("lastname: " + lastname)
        # print("totalprice: " + str(totalprice))
        # print("depositpaid: " + str(depositpaid))
        # print("checkin: " + checkin_date)
        # print("checkout: " + checkout_date)
        # print("additionalneeds: " + additionalneeds)
        # print("bookingid: " + str(bookingid))
        # print("---------------------------------------------------")
