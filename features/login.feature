@ui
Feature: User login scenarios
  
  Scenario: User login with valid credentials
    Given a user is on the login page
    When the user enters credentials "standard_user" and "secret_sauce"
    Then the user is able to login
    And the product page should load in less than 1 second
  
  Scenario: User login with invalid credentials
    Given a user is on the login page
    When the user enters credentials "standard_user" and "wrong_password"
    Then the user is not able to login
    And the user should see an error message "Epic sadface: Username and password do not match any user in this service"
  
  Scenario: User is locked out
    Given a user is on the login page
    When the user enters credentials "locked_out_user" and "secret_sauce"
    Then the user is not able to login
    And the user should see an error message "Epic sadface: Sorry, this user has been locked out."
  
  Scenario: User logout
    Given a user is on the login page
    When the user enters credentials "standard_user" and "secret_sauce"
    When the user opens the navigation menu
    And the user clicks on the logout button
    Then the user is logged out
  
  Scenario: After login, the product page should load in less than 1 second
    Given a user is on the login page
    When the user enters credentials "performance_glitch_user" and "secret_sauce"
    Then the product page should load in less than 1 second
