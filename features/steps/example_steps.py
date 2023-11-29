from selenium import webdriver
from behave import given, when, then

chrome_driver = webdriver.Chrome()

# Selenium(@ui) steps

@when('we visit google')
def step_google_nav(context):
   context.browser = chrome_driver
   context.browser.get('http://www.google.com')

@then('it should have a title "Google"')
def step_google_title(context):
   context.browser = chrome_driver
   assert context.browser.title == "Google"
