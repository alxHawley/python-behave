import requests
from behave import given, when, then

from dateutil.parser import parse


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

# Get request to ping the endpoint for healthcheck
@given('the Restful Booker API returns a {status_code:d} status code')
def step_api_available(context, status_code):    
    context.response = requests.get(base_url + ping_endpoint, headers=headers)
    assert context.response.status_code == status_code

# Get request to fetch the booking that was created
@given('a booking has been created')
def step_get_booking(context):
    context.response = requests.get(base_url + booking_endpoint + context.bookingid, headers=headers)
    assert context.response.status_code == 200
    # assert that the booking data returned matches the data used to create the booking
    assert context.response.json()["firstname"] == context.firstname
    assert context.response.json()["lastname"] == context.lastname
    assert context.response.json()["totalprice"] == context.totalprice
    assert context.response.json()["depositpaid"] == context.depositpaid
    assert context.response.json()["bookingdates"]["checkin"] == context.checkin
    assert context.response.json()["bookingdates"]["checkout"] == context.checkout
    assert context.response.json()["additionalneeds"] == context.additionalneeds


# When steps

# Post request to create a booking and add booking data to the context
@when('valid booking data is submitted to the booking endpoint')
def step_create_booking(context):
    for booking_data in context.table:  # extract the data table
        context.firstname = booking_data['firstname']
        context.lastname = booking_data['lastname']
        context.totalprice = int(booking_data['totalprice'])  # Convert to integer
        context.depositpaid = bool(booking_data['depositpaid'])  # Convert to boolean
        context.checkin = booking_data['checkin']
        context.checkout = booking_data['checkout']
        context.additionalneeds = booking_data['additionalneeds']
        
        checkin_date = parse(context.checkin).strftime('%Y-%m-%d')
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
        })


# PUT request to update a booking with a bookingid and token
@when('updated booking data is submitted to the booking endpoint')
def step_update_booking(context):
    
    for booking_data in context.table:  # extract the data table
        firstname = booking_data['firstname']
        lastname = booking_data['lastname']
        totalprice = int(booking_data['totalprice'])  # Convert to integer
        depositpaid = bool(booking_data['depositpaid'])  # Convert to boolean
        checkin = booking_data['checkin']
        checkout = booking_data['checkout']
        additionalneeds = booking_data['additionalneeds']
        
        checkin_date = parse(checkin).strftime('%Y-%m-%d')  # Convert to date format
        checkout_date = parse(checkout).strftime('%Y-%m-%d')

        headers_with_cookie["Cookie"] = f"token={context.token}"  # add the token to the headers
        context.response = requests.put(base_url + booking_endpoint + context.bookingid, headers=headers_with_cookie, json={
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


# Then steps

# Assert the status code from the response
@then('the API returns a {status_code:d} status code')
def step_response_status_code(context, status_code):
    assert context.response.status_code == status_code
    # Check if the bookingid field is present in the JSON response
    if "bookingid" in context.response.json():
        # Get the bookingid from the response then add it to the context
        bookingid = context.response.json()["bookingid"]
        context.bookingid = str(bookingid)

# Assert the booking response data returned is correct and includes the bookingid
@then('the API returns a bookingid with the booking data')
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


# Assert a valid token is returned from the auth endpoint
@then('a valid token is provided from the auth endpoint')
def step_get_token(context):
    context.response = requests.post(base_url + auth_endpoint, json={
        "username": "admin",
        "password": "password123"
    })
    context.token = context.response.json()["token"]
    # assert that the token is not empty
    assert context.token != ""
    assert context.response.status_code == 200


# Assert the booking is updated by the PUT request
@then("the booking data has been updated")
def step_get_updated_booking(context):
    # Retrieve the updated booking data from the API
    response = requests.get(base_url + booking_endpoint + context.bookingid)
    booking_data = response.json()

    # Compare the updated booking data to PUT update data
    assert booking_data["firstname"] == context.table[0]["firstname"]
    assert booking_data["lastname"] == context.table[0]["lastname"]
    assert booking_data["totalprice"] == int(context.table[0]["totalprice"])
    assert booking_data["depositpaid"] == bool(context.table[0]["depositpaid"])
    assert booking_data["bookingdates"]["checkin"] == context.table[0]["checkin"]
    assert booking_data["bookingdates"]["checkout"] == context.table[0]["checkout"]
    assert booking_data["additionalneeds"] == context.table[0]["additionalneeds"]