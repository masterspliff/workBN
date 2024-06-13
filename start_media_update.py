import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def run(playwright: Playwright) -> None:
    email = os.getenv("EMAIL_PIM")
    password = os.getenv("PASSWORD_PIM")

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://bn.cloud4.structpim.com/umbraco#/StructPIM?dashboard=Struct%20PIM%20dashboard")
    page.goto("https://bn.cloud4.structpim.com/umbraco#/login/false?dashboard=Struct%20PIM%20dashboard&returnPath=%252FStructPIM%253Fdashboard%252520PIM%252520dashboard")
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill(email)
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_role("button", name="Login").click()

    page.goto("https://bn.cloud4.structpim.com/umbraco#/StructPIM/StructPIMTree/catalogue/3df9a483-cd3f-4b7f-abaf-afe935a27923")
    page.locator("div:nth-child(3) > .pim-column-actions > .pim-floating-label-input__wrapper > .pim-floating-label-input__data > .pim-floating-label-input__input").fill("atlas")
    page.locator("div:nth-child(13) > .pim-column-actions > .pim-floating-label-input__wrapper > .pim-floating-label-input__data > .pim-floating-label-input__search-icon").click()
    page.locator("div:nth-child(13) > .pim-column-actions > .pim-floating-label-input__wrapper > .pim-floating-label-input__data > .pim-floating-label-input__input").fill("enab")
    page.goto("https://bn.cloud4.structpim.com/umbraco#/StructPIM/StructPIMTree/catalogue/3df9a483-cd3f-4b7f-abaf-afe935a27923")
    page.locator("div:nth-child(4) > .pim-column-actions > .pim-floating-label-input__wrapper > .pim-floating-label-input__data > .pim-floating-label-input__search-icon").click()
    page.locator("div:nth-child(4) > .pim-column-actions > .pim-floating-label-input__wrapper > .pim-floating-label-input__data > .pim-floating-label-input__input").fill("kon")
    page.locator("div:nth-child(4) > .pim-column-actions > .pim-floating-label-input__wrapper > .pim-floating-label-input__data > .pim-floating-label-input__input").press("Enter")
    
    # Wait for 5 seconds to ensure the page is loaded
    time.sleep(5)

    initial_setup_done = False

    while True:
        elements = page.locator("div.pim-table-row[tabindex='0']")
        num_elements = elements.count()

        if num_elements == 0:
            print("No more items on this page.")
            break

        for i in range(min(num_elements, 25)):
            nth_element = elements.nth(i)
            # Extract SKU number
            sku_text = nth_element.locator(".pim-table-cell").nth(4).inner_text()  # Adjust the locator as needed based on your HTML structure
            nth_element.click()
            time.sleep(2)

            if not initial_setup_done:
                # Initial setup steps (First instance)
                try:
                    page.get_by_role("link", name="...").click()
                    page.get_by_role("link", name="Magento connect").nth(0).click()  # Ensuring the first link is clicked
                    page.get_by_role("button", name="Start media update").click()
                    print(f"SKU: {sku_text}")  # Print SKU after clicking "Start media update"
                    initial_setup_done = True  # Mark initial setup as done
                except Exception as e:
                    print(f"Error occurred during initial setup: {e}")
            else:
                # Only click "Start media update" and "Refresh" in subsequent iterations
                try:
                    page.get_by_role("button", name="Start media update").click()
                    print(f"SKU: {sku_text}")  # Print SKU after clicking "Start media update"
                except Exception as e:
                    print(f"Error occurred during media update: {e}")

            time.sleep(2)
            
            # Go back to the search page
            page.goto("https://bn.cloud4.structpim.com/umbraco#/StructPIM/StructPIMTree/catalogue/3df9a483-cd3f-4b7f-abaf-afe935a27923")
            time.sleep(2)

        # Click on the next page button if available
        try:
            next_button = page.get_by_role("button", name="").nth(1)
            if next_button:
                next_button.click()
                time.sleep(5)  # Wait for the next page to load
                continue
        except Exception as e:
            print(f"Error occurred while trying to go to the next page: {e}")

        # If no more items and no next page button, print done and exit loop
        print("I'm done")
        break

    # Close the context and browser
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
