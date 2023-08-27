Feature: A user is able to create and manage bookings with Restful Booking.

Scenario: A user is able to create a new booking at Restful Booking.
Given the Restful Booker API is available and returns a 200 status code for the authentication endpoint
When I create the following bookings
  | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
  | John      | Doe      | 100        | true        | 2023-08-25 | 2023-08-28 | None            |
Then the response should have a 200 status code
Then the response should have the following details
  | bookingid | firstname | lastname | totalprice | depositpaid | checkin | checkout | additionalneeds |
  