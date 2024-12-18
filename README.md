# Python BDD: Test Automation with the Behave Framework, Requests, and Selenium

Welcome to my Python/Behave Test Automation project. This project is being developed to explore BDD (Behavior Driven Development) for testing backend and frontend features.

## Project details:

The API steps rely on the Python Requests library to make authentication requests, perform CRUD actions on the API, and make assertions on the API response. Additionally, I've added some schema validation steps that utilize jsonschema. For API testing I really value the simplicity, capability, and speed of Python paired with Requests.

The UI steps use Selenium to interact with a playground website. Selenium was chosen for this project simply because it works well with Python (and I wanted the exercise).

WIP: This project is set up (albeit somewhat crudely) with a GitHub Actions Workflow to run features on pushes to the main branch. I had to get a little creative with the environment.py file to isolate dependancies/imports, and I have backlog items to modify and enhance the workflow for better performance.

Backlog: additional API features/steps, refactor API features/steps, additional UI features/steps & refactor, better UI test organization, put into Docker, etc; etc;

## BDD and Behave?

Behavior-Driven Development (BDD) is a software development methodology that emphasizes collaboration between developers, testers, and domain experts to ensure the alignment of software behavior with business requirements. Behave is a Python framework that enables BDD by allowing the creation of human-readable test scenarios and automating their execution.

## Key Components of a Behave Test:

In Behave, tests are written in a natural language format called Gherkin. Each test is composed of the following key components:

- **Feature:** A high-level description of the functionality being tested.
- **Scenario:** A specific test case described in a user-readable manner.
- **Given:** The initial context or setup for the scenario.
- **When:** The action or event that occurs.
- **Then:** The expected outcome or result.

For details on how this translates into Python code, and the directory layout, please review the official documentation: https://behave.readthedocs.io/en/stable/gherkin.html#feature-testing-layout

## Setup and Dependencies:

Before you can start running tests, ensure you have the following dependencies installed:

- Python: You can download Python from the official website: https://www.python.org/downloads/
  - For Python versions 3.4 and later, utilize "pip" to manage package installations and dependencies. If you're working with older Python versions, you can install pip using these instructions: https://pip.pypa.io/en/stable/installation/

- Behave
- Requests
- Selenium
- jsonschema

Install these dependencies using the "pip install" command:

```bash
pip install behave requests selenium jsonschema
```

Or, via the requirements.txt document - just be advised I need to clean this up:

```bash
pip install -r requirements.txt
```

## Running Tests:

A note on the API environment: This feature was initially developed against the production URL. This can still be used by changing the BASE_URL in api_steps.py from:

```bash
os.getenv("BASE_URL", "http://localhost:3001/")
```

to:

```bash
"https://restful-booker.herokuapp.com/"
```

I have since changed this over to point to a local Docker image of the API . To do the same, you can get the image from: https://hub.docker.com/r/mwinteringham/restfulbooker/tags or:

```bash
docker pull mwinteringham/restfulbooker:latest
```

To run indivudal scenarios in this repository, navigate to the project's root directory and execute the following command (API feature, for example):

```bash
behave features/api.feature
```

To run all the scenarios, simply run:
```bash
behave
```

Alternatively, you can run tests based on tags. The API scenarios are tagged with @api and frontend tests are tagged @ui, for example run:

```bash
behave --tags=@api
```

## Resources:

API playground: https://restful-booker.herokuapp.com/apidoc/index.html, provided by Mark Winteringham at https://www.mwtestconsultancy.co.uk/

API Docker Image: https://hub.docker.com/r/mwinteringham/restfulbooker/tags

FE playground for Selenium: https://www.saucedemo.com/, provided by https://saucelabs.com/
