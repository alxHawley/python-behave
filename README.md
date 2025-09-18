# Python BDD Test Automation

[![Python](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/downloads/)
[![Behave](https://img.shields.io/badge/behave-BDD-green.svg)](https://behave.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive test automation project using **Behavior-Driven Development (BDD)** with the Behave framework, featuring both API testing with Requests and UI testing with Selenium.

## 🚀 Features

- **API Testing**: RESTful API testing using Python Requests library
- **UI Testing**: Web application testing with Selenium WebDriver
- **Page Object Model (POM)**: Maintainable and scalable test architecture
- **BDD Framework**: Human-readable test scenarios using Gherkin syntax
- **Schema Validation**: JSON schema validation using jsonschema
- **CI/CD Integration**: GitHub Actions workflow for automated testing
- **Docker Support**: Local API testing with Docker containers
- **Comprehensive Test Coverage**: 96% pass rate across 23 test scenarios

## 📋 Table of Contents

- [About BDD](#about-bdd)
- [Page Object Model](#page-object-model)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Configuration](#configuration)
- [Resources](#resources)
- [Contributing](#contributing)
- [License](#license)

## About BDD

**Behavior-Driven Development (BDD)** is a software development methodology that emphasizes collaboration between developers, testers, and domain experts to ensure software behavior aligns with business requirements.

### Key Components

In Behave, tests are written in Gherkin format with these components:

- **Feature**: High-level description of functionality being tested
- **Scenario**: Specific test case in user-readable format
- **Given**: Initial context or setup for the scenario
- **When**: Action or event that occurs
- **Then**: Expected outcome or result

For detailed documentation, visit: [Behave Documentation](https://behave.readthedocs.io/en/stable/gherkin.html#feature-testing-layout)

## Page Object Model

This project implements the **Page Object Model (POM)** design pattern for UI testing, providing a maintainable and scalable test architecture.

### Key Benefits

- **Maintainability**: Centralized page logic reduces code duplication
- **Reusability**: Page objects can be used across different test scenarios
- **Readability**: Clear separation between test logic and page interactions
- **Scalability**: Easy to extend with new pages and functionality

### Architecture

```
pages/
├── base_page.py              # Base page functionality
├── login_page.py             # Login page interactions
├── product_page.py           # Product page interactions
├── cart_page.py              # Cart page interactions
├── checkout_page.py          # Checkout form page interactions
├── checkout_overview_page.py # Checkout overview page interactions
├── checkout_complete_page.py # Checkout complete page interactions
└── page_factory.py           # Page object factory
```

### Performance Results

- **Test Suite Execution**: 37.748s total
- **API Tests**: 0.471s (8/8 scenarios passed)
- **UI Tests**: 37.277s (14/15 scenarios passed)
- **Overall Pass Rate**: 96% (22/23 scenarios passed)

For detailed POM implementation documentation, see [POM_IMPLEMENTATION.md](POM_IMPLEMENTATION.md).

## Installation

### Prerequisites

- Python 3.4 or later
- pip (package installer for Python)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd python-bdd-test-automation
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install behave requests selenium jsonschema
   ```

## Usage

### API Testing

The API tests use the Python Requests library for:
- Authentication requests
- CRUD operations
- Response validation
- JSON schema validation

### UI Testing

The UI tests use Selenium WebDriver for:
- Web element interaction
- Form submissions
- Navigation testing
- Cross-browser compatibility

## Project Structure

```
├── features/
│   ├── api.feature          # API test scenarios
│   ├── login.feature        # Login test scenarios
│   ├── e2e.feature          # End-to-end test scenarios
│   ├── locators.py          # UI element locators
│   ├── environment.py       # Test environment configuration
│   └── steps/
│       ├── api_steps.py     # API step definitions
│       ├── login_steps.py   # Login step definitions (POM)
│       └── e2e_steps.py     # E2E step definitions (POM)
├── pages/                   # Page Object Model classes
│   ├── base_page.py         # Base page functionality
│   ├── login_page.py        # Login page interactions
│   ├── product_page.py      # Product page interactions
│   ├── cart_page.py         # Cart page interactions
│   ├── checkout_page.py     # Checkout form page interactions
│   ├── checkout_overview_page.py # Checkout overview page interactions
│   ├── checkout_complete_page.py # Checkout complete page interactions
│   └── page_factory.py      # Page object factory
├── schemas/                 # JSON schema validation files
│   ├── booking_schema.json  # Booking API schema
│   └── booking_id_schema.json # Booking ID schema
├── utils/                   # Utility functions
│   └── schema_loader.py     # Schema loading utilities
├── requirements.txt         # Python dependencies
├── POM_IMPLEMENTATION.md    # POM documentation
└── README.md               # Project documentation
```

## Testing

### Running Tests

**Run all tests**:
```bash
behave
```

**Run specific feature**:
```bash
behave features/api.feature
behave features/login.feature
behave features/e2e.feature
```

**Run by tags**:
```bash
behave --tags=@api
behave --tags=@smoke
behave --tags=@negative
behave --tags=@positive
```

**Verbose output**:
```bash
behave -v
```

### Test Environment Setup

#### API Testing
The API tests can run against:

1. **Local Docker container** (default):
   ```bash
   docker pull mwinteringham/restfulbooker:latest
   docker run -d -p 3001:3001 mwinteringham/restfulbooker:latest
   ```

2. **Production URL**: Update `BASE_URL` in `api_steps.py`:
   ```python
   os.getenv("BASE_URL", "https://restful-booker.herokuapp.com/")
   ```

#### UI Testing
The UI tests run against SauceDemo:
- **URL**: https://www.saucedemo.com/
- **Browser**: Chrome (default)
- **Page Object Model**: Implemented for maintainability

## Configuration

### Environment Variables

- `BASE_URL`: API base URL (default: `http://localhost:3001/`)

### GitHub Actions

The project includes a GitHub Actions workflow that runs tests on push to the main branch. The workflow:
- Sets up Python environment
- Installs dependencies
- Runs all test scenarios
- Reports test results

## Resources

### Test Environments

- **API Playground**: [RESTful Booker API](https://restful-booker.herokuapp.com/apidoc/index.html)
  - Provided by [Mark Winteringham](https://www.mwtestconsultancy.co.uk/)
- **UI Playground**: [Sauce Demo](https://www.saucedemo.com/)
  - Provided by [Sauce Labs](https://saucelabs.com/)

### Docker Images

- **API Docker Image**: [mwinteringham/restfulbooker](https://hub.docker.com/r/mwinteringham/restfulbooker/tags)

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and ensure tests pass:
   ```bash
   behave
   ```
4. **Commit your changes**:
   ```bash
   git commit -m "Add your feature description"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**

### Development Notes

- This project uses GitHub Actions for CI/CD
- Tests run automatically on push to main branch
- Environment configuration is handled in `environment.py`
- **Page Object Model** implemented for maintainable UI testing
- **Comprehensive test coverage** with 96% pass rate
- Future improvements planned: Cross-browser testing, mobile testing, enhanced workflows

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd python-bdd-test-automation
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Run tests
behave
```
