Feature: a couple of example scenarios

@ui
Scenario: visit google and check page title
When we visit google
Then it should have a title "Google"
