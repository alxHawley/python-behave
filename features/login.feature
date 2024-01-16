Feature: User login on saucedemo
  As a user of saucedemo.com
  I want to be able to interact with the website
  So that I can buy some products


  @ui @login @performance
  Scenario: User login with valid credentials
    Given a user is on the login page
    When the user submits credentials "standard_user" and "secret_sauce"
    Then the user is able to login
    And the product page should load in less than 1 second

  @ui @login
  Scenario: User login with invalid credentials
    Given a user is on the login page
    When the user submits credentials "standard_user" and "wrong_password"
    Then the user is not able to login
    And the user should see an error message "Epic sadface: Username and password do not match any user in this service"

  @ui @login
  Scenario: User is locked out
    Given a user is on the login page
    When the user submits credentials "locked_out_user" and "secret_sauce"
    Then the user is not able to login
    And the user should see an error message "Epic sadface: Sorry, this user has been locked out."

  @ui @login
  Scenario: User logout
    Given a user is on the login page
    When the user submits credentials "standard_user" and "secret_sauce"
    When the user opens the navigation menu
    And the user clicks on the logout button
    Then the user is logged out

  @login @performance
  Scenario: After login, the product page should load in less than 1 seconds
    Given a user is on the login page
    When the user submits credentials "performance_glitch_user" and "secret_sauce"
    Then the product page should load in less than 1 second
