Feature: Hotel bookings can be managed via the Restful Booker API
  As an API client
  I want to create, update, and delete bookings
  So that I can manage bookings with Restful Booker

Background: Create a booking
Given the Restful Booker API returns a 201 status code
When valid booking data is submitted to the booking endpoint
  | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
  | John      | Doe      | 100        | true        | 2023-08-25 | 2023-08-28 | None            |
Then the API returns a 200 status code
Then the API returns a bookingid with the booking data
  | bookingid | firstname | lastname | totalprice | depositpaid | checkin | checkout | additionalneeds |
And a valid token is provided from the auth endpoint

@api
Scenario: Update a booking
Given a booking has been created
When updated booking data is submitted to the booking endpoint
  | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
  | Jon       | Doh      | 250        | true        | 2023-08-25 | 2023-08-31 | Extra towels    |
Then the API returns a 200 status code
And the booking data has been updated
  | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
  | Jon       | Doh      | 250        | true        | 2023-08-25 | 2023-08-31 | Extra towels    |

@api
Scenario: Partial update a booking
Given a booking has been created
When partial updated booking data is submitted to the booking endpoint
  | totalprice | depositpaid | checkin    | checkout   |
  | 700        | true        | 2023-08-25 | 2023-09-25 | 
Then the API returns a 200 status code
And the booking data has been updated
  | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
  | John      | Doe      | 700        | true        | 2023-08-25 | 2023-09-25 | None            |