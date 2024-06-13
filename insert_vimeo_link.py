import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
from dotenv import load_dotenv
import os

load_dotenv()

def run(playwright: Playwright) -> None:

    username = os.getenv("USERNAME_MAGENTO")
    password = os.getenv("PASSWORD_MAGENTO")

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.bedrenaetter.dk/bnbackoffice/admin/dashboard/index/key/4684be1495569733802a9840be22b4adafe301b46d40e70bf6447753ecad0854/")
    page.get_by_placeholder("user name").click()
    page.get_by_placeholder("user name").fill(username)
    page.get_by_placeholder("password").click()
    page.get_by_placeholder("password").fill(password)
    page.get_by_role("button", name="Log ind").click()

    # Wait for the Incoming Message button to be available and click it
    incoming_message_button = page.get_by_label("Incoming Message").get_by_role("button", name="")
    expect(incoming_message_button).to_be_visible()
    incoming_message_button.click()

    # Wait for the Catalog link to be available and click it
    catalog_link = page.get_by_role("link", name=" Catalog")
    expect(catalog_link).to_be_visible()
    catalog_link.click()

    # Wait for the Products link to be available and click it
    products_link = page.get_by_role("link", name="Products", exact=True)
    expect(products_link).to_be_visible()
    products_link.click()

    # Wait for 7 seconds to ensure the page is loaded
    time.sleep(7)

    # Print out all filter buttons found
    filter_buttons = page.locator('button:has-text("Filters")')
    for index in range(filter_buttons.count()):
        print(f"Filter button {index + 1} text: {filter_buttons.nth(index).inner_text()}")

    # Refine the locator for the Filters button to avoid ambiguity
    filters_button = filter_buttons.nth(0)  # Adjust this index based on printed texts
    expect(filters_button).to_be_visible()
    filters_button.click()
    
    # Proceed to click on the "URL Key" input
    url_key_input = page.get_by_role("textbox", name="URL Key")
    expect(url_key_input).to_be_visible()
    url_key_input.click()
    url_key_input.fill("venus-ele")

    # Wait for the Apply Filters button to be available and click it
    apply_filters_button = page.get_by_role("button", name="Apply Filters")
    expect(apply_filters_button).to_be_visible()
    apply_filters_button.click()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
