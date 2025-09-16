@api
Feature: Hotel Booking Management
  As a hotel booking system user
  I want to manage hotel bookings
  So that I can create, view, update, and cancel reservations

  Background:
    Given I have valid booking credentials
    And I have a new hotel booking with the following details
      | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
      | John      | Doe      | 100        | true        | 2023-08-25 | 2023-08-28 | Breakfast       |

  @smoke @create
  Scenario: Create a new hotel booking
    When I create the booking
    Then the booking should be created successfully
    And I should receive a booking confirmation

  @smoke @read
  Scenario: Retrieve booking details
    Given a booking has been created
    When I request the booking details
    Then I should receive the correct booking information
    And the booking data should be valid

  @update @full
  Scenario: Update booking with complete information
    Given a booking has been created
    And I have updated booking details
      | firstname | lastname | totalprice | depositpaid | checkin    | checkout   | additionalneeds |
      | Jon       | Doh      | 350        | false       | 2023-08-24 | 2023-09-01 | 9 towels        |
    When I update the booking
    Then the booking should be updated successfully
    And I should receive the updated booking details
    And the booking data should be valid

  @update @partial
  Scenario: Partially update booking information
    Given a booking has been created
    And I want to update specific booking details
      | totalprice | depositpaid | checkin    | checkout   |
      | 700        | true        | 2023-08-24 | 2023-09-15 |
    When I partially update the booking
    Then the booking should be updated successfully
    And I should receive the updated booking details

  @delete
  Scenario: Cancel a hotel booking
    Given a booking has been created
    When I cancel the booking
    Then the booking should be cancelled successfully
    And the booking should no longer be accessible

  @error @invalid-id
  Scenario: Attempt to retrieve non-existent booking
    Given I have an invalid booking reference
    When I request the booking details
    Then I should receive a not found error

  @error @unauthorized
  Scenario: Attempt to update booking without authorization
    Given a booking has been created
    And I do not have valid authorization
    When I attempt to update the booking
    Then I should receive an unauthorized error
  