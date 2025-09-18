# Page Object Model Implementation

## Overview
This document outlines the Page Object Model (POM) implementation for the Selenium aspect of this project (e2e and login feature files). The POM pattern provides a maintainable and scalable architecture for UI test automation.

## Architecture

### Core Components
- **`BasePage`**: Abstract base class containing common functionality
- **`PageFactory`**: Factory pattern for creating and managing page objects
- **Page-specific classes**: `LoginPage`, `ProductPage`, `CartPage`, `CheckoutPage`, `CheckoutOverviewPage`, `CheckoutCompletePage`

### Key Benefits

#### 1. **Separation of Concerns**
- Page objects encapsulate page-specific logic
- Step definitions focus on test flow rather than implementation details
- Clear boundaries between test logic and page interactions

#### 2. **Reusability**
- Centralized page interactions in page objects
- Page objects can be used across different test scenarios
- Consistent API across all pages

#### 3. **Maintainability**
- Changes to page structure only require updating the relevant page object
- Reduced code duplication and improved consistency
- Easier to extend with new pages and functionality

#### 4. **Readability**
- Intuitive method names: `login_page.enter_username(username)`
- Clear separation between test steps and page interactions
- Self-documenting code structure

## File Structure

```
pages/
├── __init__.py
├── base_page.py              # Base page functionality
├── login_page.py             # Login page interactions
├── product_page.py           # Product page interactions
├── cart_page.py              # Cart page interactions
├── checkout_page.py          # Checkout form page interactions
├── checkout_overview_page.py # Checkout overview page interactions
├── checkout_complete_page.py # Checkout complete page interactions
└── page_factory.py           # Page object factory

features/steps/
├── login_steps.py        # Login step definitions (POM-based)
└── e2e_steps.py          # E2E step definitions (POM-based)
```

## Usage Examples

### Step Definition with POM
```python
@given("a user is on the login page")
def step_login_page(context):
    page_factory = get_page_factory(context)
    login_page = page_factory.login_page
    login_page.go_to_login_page()
    assert login_page.is_login_page_displayed()
```

### Page Object Method
```python
def go_to_login_page(self) -> None:
    """Navigate to the login page"""
    self.driver.get("https://www.saucedemo.com/")
    self.wait_for_element_visible(Locators.LOGIN_BUTTON)

def is_login_page_displayed(self) -> bool:
    """Check if login page is displayed"""
    return self.is_element_visible(Locators.LOGIN_BUTTON)
```

### Factory Pattern Usage
```python
def get_page_factory(context):
    """Get or create PageFactory instance"""
    if not hasattr(context, 'page_factory'):
        context.page_factory = PageFactory(context.browser)
    return context.page_factory
```

## Page Object Classes

### BasePage
The foundation class providing common functionality:
- Element finding and waiting methods
- Click and text input operations
- URL navigation and validation
- Logging and error handling

### LoginPage
Handles all login-related interactions:
- Navigation to login page
- Username and password input
- Login button interaction
- Error message handling
- Login validation

### ProductPage
Manages product catalog interactions:
- Product page validation
- Navigation menu operations
- Logout functionality
- Product addition to cart
- Cart navigation

### CartPage
Handles shopping cart operations:
- Cart page validation
- Product verification in cart
- Checkout initiation

### CheckoutPage
Manages checkout form interactions:
- Checkout information input
- Form validation
- Continue button interaction

### CheckoutOverviewPage
Handles checkout review:
- Order summary validation
- Finish button interaction

### CheckoutCompletePage
Manages completion flow:
- Success page validation
- Order confirmation

### PageFactory
Factory pattern implementation:
- Singleton page object management
- Lazy loading of page objects
- Context-based page retrieval

## Performance Considerations

- **Lazy Loading**: Page objects are created only when needed
- **Caching**: Page objects are cached in PageFactory for reuse
- **Efficient Waits**: Centralized wait strategies in BasePage
- **Memory Management**: Proper cleanup of page objects

## Best Practices

1. **Single Responsibility**: Each page object handles one specific page
2. **DRY Principle**: Common functionality centralized in BasePage
3. **Factory Pattern**: Centralized page object creation and management
4. **Consistent Naming**: Clear, descriptive method and variable names
5. **Error Handling**: Comprehensive error handling and logging
6. **Type Hints**: Better code documentation and IDE support
7. **Explicit Waits**: Reliable element interaction with proper waiting
8. **Locator Management**: Centralized locator definitions for maintainability
