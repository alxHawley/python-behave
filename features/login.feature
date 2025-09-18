@ui
Feature: User Authentication
  As a user of the SauceDemo application
  I want to authenticate securely
  So that I can access the product catalog and manage my session

  Background:
    Given a user is on the login page

  @smoke @positive
  Scenario: Successful login with valid credentials
    When the user enters "standard_user" and "secret_sauce"
    Then the user should be successfully logged in
    And the product page should be displayed
    And the product page should load in less than 1 second

  @smoke @negative
  Scenario: Failed login with invalid credentials
    When the user enters "standard_user" and "wrong_password"
    Then the user should not be able to login
    And the user should see an error message "Epic sadface: Username and password do not match any user in this service"

  @negative @security
  Scenario: Login attempt with locked out user
    When the user enters "locked_out_user" and "secret_sauce"
    Then the user should not be able to login
    And the user should see an error message "Epic sadface: Sorry, this user has been locked out."

  @negative @validation
  Scenario: Login attempt with empty credentials
    When the user enters "" and ""
    Then the user should not be able to login
    And the user should see an error message "Epic sadface: Username is required"

  @negative @validation
  Scenario: Login attempt with empty username
    When the user enters "" and "secret_sauce"
    Then the user should not be able to login
    And the user should see an error message "Epic sadface: Username is required"

  @negative @validation
  Scenario: Login attempt with empty password
    When the user enters "standard_user" and ""
    Then the user should not be able to login
    And the user should see an error message "Epic sadface: Password is required"

  @smoke @session
  Scenario: User logout functionality
    Given the user is logged in with "standard_user" and "secret_sauce"
    When the user opens the navigation menu
    And the user clicks on the logout button
    Then the user should be logged out
    And the user should be redirected to the login page

  @performance @glitch-user
  Scenario: Performance test with glitch user
    When the user enters "performance_glitch_user" and "secret_sauce"
    Then the user should be successfully logged in
    And the product page should load in less than 3 seconds

  @data-driven @credentials
  Scenario Outline: Login with different user types
    When the user enters "<username>" and "<password>"
    Then the user should be "<expected_result>"
    And the user should see "<error_message>"

    Examples:
      | username           | password      | expected_result | error_message                                                                 |
      | standard_user      | secret_sauce  | successfully logged in |                                                                        |
      | locked_out_user    | secret_sauce  | not able to login | Epic sadface: Sorry, this user has been locked out.                        |
      | problem_user       | secret_sauce  | successfully logged in |                                                                        |
      | performance_glitch_user | secret_sauce | successfully logged in |                                                                    |
