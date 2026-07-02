"""
Selenium script to upload digital signature image for company location mappings.

GLOBAL VARIABLES - Configure these before running:
"""

# ─────────────────────────────────────────────
#  GLOBAL CONFIGURATION
# ─────────────────────────────────────────────

LOGIN_URL          = "https://api.ezycomp.com/admin/login"
LISTING_URL        = "https://api.ezycomp.com/admin/company_location_mappings?q%5Bparent_company_eq%5D=591971c0-b24a-4afe-8e72-6ecc4c0b2c95&q%5Bcompany_id_eq%5D=a48b4169-05a6-4d3d-ae55-54e9e3c98b41&commit=Filter&order=created_at_desc"

EMAIL              = "yash.harne@cielhr.com"
PASSWORD           = "Ezycomp@1234"

TARGET_COMPANY     = "QA Test RG Company"          # Associate company name to filter
SIGNATURE_IMAGE    = r"C:\Users\Yash Harne\Downloads\Sign.jpg"  # Full path to the signature image

MAX_LOCATIONS      = 70   # ← CHANGE THIS: how many location records to update (0 = all)
                         #   Set to 0 to process every matching record on every page.

HEADLESS           = False   # Set True to run Chrome without a visible window
PAGE_LOAD_TIMEOUT  = 30      # seconds
ELEMENT_WAIT       = 15      # seconds for explicit waits

# ─────────────────────────────────────────────
#  IMPORTS
# ─────────────────────────────────────────────

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)

# Try to auto-manage chromedriver; fall back to system PATH if unavailable.
try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_DRIVER_MANAGER = True
except ImportError:
    USE_DRIVER_MANAGER = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def build_driver() -> webdriver.Chrome:
    """Return a configured Chrome WebDriver instance."""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,900")
    # Allow file chooser to be triggered programmatically
    options.add_experimental_option("prefs", {"safebrowsing.enabled": True})

    if USE_DRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver


def wait_for(driver, by, selector, timeout=ELEMENT_WAIT):
    """Wait until an element is present and visible, then return it."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )


def login(driver: webdriver.Chrome) -> None:
    """Log in to the admin panel."""
    log.info("Navigating to login page …")
    driver.get(LOGIN_URL)

    wait_for(driver, By.ID, "admin_user_email").send_keys(EMAIL)
    driver.find_element(By.ID, "admin_user_password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "commit").click()

    # Wait until we are redirected away from the login page
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        lambda d: "login" not in d.current_url
    )
    log.info("Login successful.")


def get_edit_links_on_page(driver: webdriver.Chrome) -> list[tuple[str, str]]:
    """
    Parse the current listing page and return a list of (company_name, edit_href)
    tuples for rows whose associate company matches TARGET_COMPANY.
    """
    results = []
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    except NoSuchElementException:
        return results

    for row in rows:
        try:
            company_cell = row.find_element(By.CSS_SELECTOR, "td.col.col-company")
            company_name = company_cell.text.strip()
        except NoSuchElementException:
            continue

        if company_name != TARGET_COMPANY:
            continue

        try:
            edit_link = row.find_element(By.CSS_SELECTOR, "a.edit_link")
            results.append((company_name, edit_link.get_attribute("href")))
        except NoSuchElementException:
            log.warning("Matching row found but no edit link – skipping.")

    return results


def next_page_url(driver: webdriver.Chrome) -> str | None:
    """Return the href of the 'Next ›' pagination link, or None if on last page."""
    try:
        next_link = driver.find_element(
            By.CSS_SELECTOR, "a[rel='next'], .next_page a, li.next a"
        )
        return next_link.get_attribute("href")
    except NoSuchElementException:
        return None


def upload_signature(driver: webdriver.Chrome, edit_url: str) -> bool:
    """
    Open the edit page, upload the signature image, and submit the form.
    Returns True on success, False on failure.
    """
    log.info("Opening edit page: %s", edit_url)
    driver.get(edit_url)

    # ── Locate the file input ──────────────────────────────────────────────
    try:
        file_input = WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.presence_of_element_located(
                (By.ID, "company_location_mapping_digital_signature")
            )
        )
    except TimeoutException:
        log.error("File input not found on edit page.")
        return False

    # Make the input visible in case it is hidden (common with styled file inputs)
    driver.execute_script(
        "arguments[0].style.display = 'block';"
        "arguments[0].style.visibility = 'visible';"
        "arguments[0].style.opacity = '1';",
        file_input,
    )
    time.sleep(0.5)

    # Send the absolute path of the image file
    abs_path = os.path.abspath(SIGNATURE_IMAGE)
    if not os.path.isfile(abs_path):
        log.error("Signature image not found at: %s", abs_path)
        return False

    file_input.send_keys(abs_path)
    log.info("Signature image sent to file input.")
    time.sleep(1)

    # ── Submit the form ────────────────────────────────────────────────────
    try:
        submit_btn = driver.find_element(
            By.CSS_SELECTOR, "input[name='commit'][value='Update Company location mapping']"
        )
        submit_btn.click()
        log.info("Form submitted.")
    except NoSuchElementException:
        log.error("Submit button not found.")
        return False

    # Wait for redirect back to listing or a flash notice
    try:
        WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
            lambda d: "edit" not in d.current_url or
                      d.find_elements(By.CSS_SELECTOR, ".flash_notice, .notice, #flash_notice")
        )
        log.info("Update completed successfully.")
        return True
    except TimeoutException:
        log.warning("Timed out waiting for post-submit redirect, but continuing.")
        return True


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main() -> None:
    if not os.path.isfile(os.path.abspath(SIGNATURE_IMAGE)):
        log.error(
            "Signature image not found at '%s'. "
            "Please update the SIGNATURE_IMAGE variable and try again.",
            SIGNATURE_IMAGE,
        )
        return

    driver = build_driver()
    updated_count = 0

    try:
        login(driver)

        current_page_url = LISTING_URL

        while current_page_url:
            log.info("Loading listing page: %s", current_page_url)
            driver.get(current_page_url)
            time.sleep(2)  # Let the table render

            edit_links = get_edit_links_on_page(driver)
            log.info(
                "Found %d matching record(s) for '%s' on this page.",
                len(edit_links),
                TARGET_COMPANY,
            )

            for company_name, edit_href in edit_links:
                if MAX_LOCATIONS > 0 and updated_count >= MAX_LOCATIONS:
                    log.info(
                        "Reached MAX_LOCATIONS limit (%d). Stopping.", MAX_LOCATIONS
                    )
                    return

                log.info(
                    "[%d] Updating record for: %s", updated_count + 1, company_name
                )
                success = upload_signature(driver, edit_href)
                if success:
                    updated_count += 1
                    log.info("Total updated so far: %d", updated_count)
                else:
                    log.warning("Failed to update record at: %s", edit_href)

                # Return to listing for next iteration
                driver.get(LISTING_URL)
                time.sleep(2)

            # Check for next pagination page
            # Re-navigate to same page URL to get fresh pagination links
            driver.get(current_page_url)
            time.sleep(1)
            next_url = next_page_url(driver)

            if next_url and (MAX_LOCATIONS == 0 or updated_count < MAX_LOCATIONS):
                current_page_url = next_url
            else:
                break

        log.info("Done. Total records updated: %d", updated_count)

    except Exception as exc:
        log.exception("Unexpected error: %s", exc)
    finally:
        driver.quit()
        log.info("Browser closed.")


if __name__ == "__main__":
    main()