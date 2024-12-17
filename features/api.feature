@api
Feature: API CRUD operations  
  As an API client I can create, read, update, and delete hotel bookings

Background:
    Given a post request is made to /booking with the following payload
    | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
    | John      | Doe      | 100        | true        | 2023-08-25 | 2023-08-28 | None            |
    When the response is returned
    Then a booking ID is generated
    And an auth token is generated
  
  Scenario: GET request with booking ID
    When a GET request is made with the booking ID
    Then the API response returns the correct record details

  Scenario: PUT request with booking ID
    When a PUT request is made with a booking ID and an updated payload
    | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
    | Jon       | Doh      | 350        | false       | 2023-08-24 | 2023-09-01 | 9 towels        |
    Then the API response returns the correct record details
    And the json schema for the record is valid

  Scenario: PATCH request with booking ID
    When a PATCH request is made with the booking ID
    | totalprice | depositpaid | checkin    | checkout   |
    | 700        | true        | 2023-08-24 | 2023-09-15 |
    Then the API response returns the new record details

  Scenario: DELETE request with booking ID
    When a DELETE request is made with the booking ID
    Then the record is deleted

  # create scenarios forGetBookingIds, GetBookingIdsWithParams, GetBookingIdsWithInvalidParams
  # params: firstmane, lastname, checkin, checkout
  