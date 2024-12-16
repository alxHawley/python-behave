@api
Feature: Hotel bookings management with Restful Booker API  
  As an API client
  I want to create, update, and delete hotel bookings
  So that I can manage bookings with Restful Booker

Background:
    Given a hotel booking is created
    | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
    | John      | Doe      | 100        | true        | 2023-08-25 | 2023-08-28 | None            |
    When the booking details are provided
    Then a booking ID is obtained
    And an auth token is obtained
  
  Scenario: Retrieving booking details
    When a GET request is made with the booking ID
    Then the booking details are retrieved successfully

  Scenario: Updating booking details
    When a PUT request is made with the booking ID
    | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
    | Jon       | Doh      | 350        | false       | 2023-08-24 | 2023-09-01 | 9 towels        |
    Then the booking details are updated successfully
    And the booking details are retrieved successfully

  Scenario: Partially updating booking details
    When a PATCH request is made with the booking ID
    | totalprice | depositpaid | checkin    | checkout   |
    | 700        | true        | 2023-08-24 | 2023-09-15 |
    Then the booking details are partially updated successfully

  Scenario: Deleting a booking
    When a DELETE request is made with the booking ID
    Then the booking is deleted successfully

  # create scenarios forGetBookingIds, GetBookingIdsWithParams, GetBookingIdsWithInvalidParams
  # params: firstmane, lastname, checkin, checkout
  