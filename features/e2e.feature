Feature: User purchase flow

Background: User is logged in
    Given a user is on the login page
    When the user enters credentials "standard_user" and "secret_sauce"
    Then the user is able to login

  @e2e @ui
  Scenario Outline: User adds a product to the cart and checks out
    When the user adds the product "<product_name>" to the cart
    And the user clicks on the cart icon
    Then the product "<product_name>" is in the cart
    When the user clicks checkout
    Then the checkout page loads
    When the user enters their information
      | First Name | Last Name | Zip/Postal Code |
      | John       | Doe       | 12345           |
    And the user clicks continue
    Then the checkout overview page loads
    When the user clicks finish
    Then the confirmation page loads

    Examples:
      | product_name           |
      | Sauce Labs Backpack    |
      | Sauce Labs Bike Light  |
      | Sauce Labs Bolt T-Shirt|
