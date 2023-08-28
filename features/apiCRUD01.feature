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
  
  @api
  Scenario: Retrieving booking details
    When a GET request is made with the booking ID
    Then the booking details are retrieved successfully

  @api
  Scenario: Updating booking details
    When a PUT request is made with the booking ID
    And new booking details are provided
    Then the booking details are updated successfully

  @api
  Scenario: Partially updating booking details
    When a PATCH request is made with the booking ID
    And partial booking details are provided
    Then the booking details are partially updated successfully

  @api
  Scenario: Deleting a booking
    When a DELETE request is made with the booking ID
    Then the booking is deleted successfully
