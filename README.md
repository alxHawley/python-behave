# PythonBDD Test Repository

Welcome to my Python BDD project. This test automation project is developed with Behave, a Python-based Behavior-Driven Development (BDD) testing framework. Currently there are 3 features that include 10 scenarios across API tests and UI tests with Selenium.

API used for backend automation: https://restful-booker.herokuapp.com/apidoc/index.html

This is a mock hotel booking API.

Site for Selenium automation : https://www.saucedemo.com/

This is a mock e-commerce site

## What is BDD and Behave?

Behavior-Driven Development (BDD) is a software development methodology that emphasizes collaboration between developers, testers, and domain experts to ensure the alignment of software behavior with business requirements. Behave is a Python framework that enables BDD by allowing the creation of human-readable test scenarios and automating their execution.

## Key Components of a Behave Test:

In Behave, tests are written in a natural language format called Gherkin. Each test is composed of the following key components:

- **Feature:** A high-level description of the functionality being tested.
- **Scenario:** A specific test case described in a user-readable manner.
- **Given:** The initial context or setup for the scenario.
- **When:** The action or event that occurs.
- **Then:** The expected outcome or result.

For details on how this translate into Python, please review the official documentation: https://behave.readthedocs.io/en/stable/gherkin.html#feature-testing-layout

## Setup and Dependencies:

Before you can start running tests, ensure you have the following dependencies installed:

- Python: You can download Python from the official website: https://www.python.org/downloads/
  - For Python versions 3.4 and later, utilize "pip" to manage package installations and dependencies. If you're working with older Python versions, you can install pip using these instructions: https://pip.pypa.io/en/stable/installation/

- Behave
- Requests
- Selenium

With pip, You can install these dependencies using the "pip install" command, ie;

```bash
pip install behave requests selenium
```

## Running Tests:

To run the scenarios included in this repository, navigate to the project's root directory and execute the following command (API feature, for example):

```bash
behave features/api.feature
```

Alternatively, you can run tests based on how they are tagged. The API scenarios are tagged with @api and FE tests as @ui. As the Selenium tests are added, more tags will be added - so far, @login and @performance have been created. An example of running the @api tagged scenarios:

```bash
behave --tags=@api
```

## Resources:

As the development of this project progresses, this README will be continuously updated to provide more detailed information and additional resources.

If you have any questions or suggestions please feel free reach out to me directly.
