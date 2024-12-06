Feature: User login on saucedemo
  As a user of saucedemo.com
  I want to be able to interact with the website
  So that I can buy some products

Background: User login performed
    Given a user is on the login page
    When the user submits credentials "standard_user" and "secret_sauce"
    Then the user is able to login


  @e2e
  Scenario: User purchase flow
    When the user adds a product to the cart
    And the user clicks on the cart icon
    Then the user is able to see the item in the cart
    When the user clicks on the checkout button
    Then the user is able to see the checkout page
    When the user fills the form with the following data
      | First Name | Last Name | Zip/Postal Code |
      | John       | Doe       | 12345           |
    And the user clicks on the continue button
    Then the user is able to see the overview page
    When the user clicks on the finish button
    Then the user is able to see the confirmation page
