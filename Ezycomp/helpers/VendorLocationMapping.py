# =============================================================
#  Vendor Location Mapping — Auto-create for ALL locations
#  Uses exact element IDs from the actual HTML form
# =============================================================

# ─────────────────────────────────────────────
#  GLOBAL CONFIGURATION
# ─────────────────────────────────────────────

LOGIN_URL       = "https://ezycompapi.ur-nl.com/admin/login"
NEW_MAPPING_URL = "https://ezycompapi.ur-nl.com/admin/vendor_location_mappings/new"

EMAIL    = "yash.harne@cielhr.com"
PASSWORD = "Ezycomp@1234"

# ── Exact option VALUES from the HTML (not visible text) ──────
# Company: "CLRA Registers Management Pvt Ltd"
COMPANY_VALUE             = "3073934b-82ec-454a-8cd2-5283096d02d7"

# Associate Company: "CLRA Associates 2"  (populated via AJAX after company selection)
# We match by visible text since options load dynamically
ASSOCIATE_COMPANY_TEXT    = "CLRA Associates 2"

# Vendor Category: "Security Services"
VENDOR_CATEGORY_VALUE     = "08e4df2d-2fd5-4175-b2f6-4e6cc01ff400"

# Vendor Registration: "CLRA Vendor 1"
VENDOR_REGISTRATION_VALUE = "234ee7d1-ecd8-49ee-988a-521f3ae0ef8d"

# 0 = process ALL locations; e.g. 3 = test with first 3 only
MAX_LOCATIONS = 68

HEADLESS          = False
PAGE_LOAD_TIMEOUT = 30
ELEMENT_WAIT      = 20   # seconds to wait for AJAX dropdowns

# ─────────────────────────────────────────────

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

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
#  DRIVER
# ─────────────────────────────────────────────

def build_driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,900")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    if USE_DRIVER_MANAGER:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────

def login(driver):
    log.info("Logging in ...")
    driver.get(LOGIN_URL)
    WebDriverWait(driver, ELEMENT_WAIT).until(
        EC.presence_of_element_located((By.ID, "admin_user_email"))
    ).send_keys(EMAIL)
    driver.find_element(By.ID, "admin_user_password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "commit").click()
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        lambda d: "login" not in d.current_url
    )
    log.info("Login successful.")


# ─────────────────────────────────────────────
#  WAIT HELPERS
# ─────────────────────────────────────────────

def wait_until_enabled(driver, element_id, timeout=ELEMENT_WAIT):
    """Wait until a select is no longer disabled (AJAX finished loading)."""
    WebDriverWait(driver, timeout).until(
        lambda d: not d.find_element(By.ID, element_id).get_attribute("disabled")
    )

def wait_until_has_options(driver, element_id, min_real_options=1, timeout=ELEMENT_WAIT):
    """
    Wait until a select has at least min_real_options non-blank options.
    Real options = options with a non-empty value.
    """
    def check(d):
        try:
            sel = Select(d.find_element(By.ID, element_id))
            real = [o for o in sel.options if o.get_attribute("value").strip()]
            return len(real) >= min_real_options
        except Exception:
            return False
    WebDriverWait(driver, timeout).until(check)


# ─────────────────────────────────────────────
#  READ ALL LOCATIONS  (called once at startup)
# ─────────────────────────────────────────────

def get_all_locations(driver):
    """
    Opens the new form, selects Company + Associate Company,
    then reads every real option from the Location dropdown (id=companyLocations).
    Returns list of (value, text) tuples.
    """
    log.info("Opening form to read all locations ...")
    driver.get(NEW_MAPPING_URL)
    time.sleep(2)

    # 1. Select Company by exact value
    log.info("  Selecting Company ...")
    company_sel = Select(
        WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.presence_of_element_located((By.ID, "vendor_location_mapping_company_id"))
        )
    )
    company_sel.select_by_value(COMPANY_VALUE)
    log.info("  Company selected.")

    # 2. Wait for Associate Company dropdown to become enabled & populated
    log.info("  Waiting for Associate Company to load ...")
    wait_until_enabled(driver, "associateCompany")
    wait_until_has_options(driver, "associateCompany", min_real_options=1)
    time.sleep(1)

    assoc_sel = Select(driver.find_element(By.ID, "associateCompany"))
    # Find option matching ASSOCIATE_COMPANY_TEXT (partial, case-insensitive)
    assoc_text_lower = ASSOCIATE_COMPANY_TEXT.lower()
    assoc_matched = False
    for opt in assoc_sel.options:
        if assoc_text_lower in opt.text.strip().lower():
            assoc_sel.select_by_value(opt.get_attribute("value"))
            log.info("  Associate Company selected: '%s'", opt.text.strip())
            assoc_matched = True
            break
    if not assoc_matched:
        available = [o.text.strip() for o in assoc_sel.options if o.text.strip()]
        raise RuntimeError(
            f"Associate Company '{ASSOCIATE_COMPANY_TEXT}' not found.\nAvailable: {available}"
        )

    # 3. Wait for Location dropdown to become enabled & populated
    log.info("  Waiting for Location dropdown to load ...")
    wait_until_enabled(driver, "companyLocations")
    wait_until_has_options(driver, "companyLocations", min_real_options=1)
    time.sleep(1)

    loc_select = Select(driver.find_element(By.ID, "companyLocations"))
    locations = [
        (opt.get_attribute("value"), opt.text.strip())
        for opt in loc_select.options
        if opt.get_attribute("value").strip() and opt.text.strip()
    ]

    log.info("Found %d location(s):", len(locations))
    for i, (val, txt) in enumerate(locations, 1):
        log.info("  [%d] %s", i, txt)

    return locations


# ─────────────────────────────────────────────
#  CREATE ONE MAPPING
# ─────────────────────────────────────────────

def create_mapping(driver, loc_value, loc_text, index, total):
    """Fill and submit the form for one location. Returns True on success."""
    log.info("--- [%d/%d] Location: '%s' ---", index, total, loc_text)
    driver.get(NEW_MAPPING_URL)
    time.sleep(2)

    try:
        # ── 1. Company ────────────────────────────────────────────────
        Select(
            WebDriverWait(driver, ELEMENT_WAIT).until(
                EC.presence_of_element_located((By.ID, "vendor_location_mapping_company_id"))
            )
        ).select_by_value(COMPANY_VALUE)
        log.info("  [1/5] Company set.")

        # ── 2. Associate Company ──────────────────────────────────────
        wait_until_enabled(driver, "associateCompany")
        wait_until_has_options(driver, "associateCompany", min_real_options=1)
        time.sleep(0.5)

        assoc_sel = Select(driver.find_element(By.ID, "associateCompany"))
        assoc_text_lower = ASSOCIATE_COMPANY_TEXT.lower()
        for opt in assoc_sel.options:
            if assoc_text_lower in opt.text.strip().lower():
                assoc_sel.select_by_value(opt.get_attribute("value"))
                break
        log.info("  [2/5] Associate Company set.")

        # ── 3. Location ───────────────────────────────────────────────
        wait_until_enabled(driver, "companyLocations")
        wait_until_has_options(driver, "companyLocations", min_real_options=1)
        time.sleep(0.5)

        Select(driver.find_element(By.ID, "companyLocations")).select_by_value(loc_value)
        log.info("  [3/5] Location set: '%s'", loc_text)

        # ── 4. Vendor Category ────────────────────────────────────────
        Select(
            WebDriverWait(driver, ELEMENT_WAIT).until(
                EC.presence_of_element_located(
                    (By.ID, "vendor_location_mapping_vendor_category_id")
                )
            )
        ).select_by_value(VENDOR_CATEGORY_VALUE)
        log.info("  [4/5] Vendor Category set.")

        # ── 5. Vendor Registration ────────────────────────────────────
        Select(
            WebDriverWait(driver, ELEMENT_WAIT).until(
                EC.presence_of_element_located(
                    (By.ID, "vendor_location_mapping_vendor_registration_id")
                )
            )
        ).select_by_value(VENDOR_REGISTRATION_VALUE)
        log.info("  [5/5] Vendor Registration set.")

        # ── Submit ────────────────────────────────────────────────────
        submit = WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='commit']"))
        )
        submit.click()
        log.info("  Form submitted.")

        # Wait for redirect away from /new (success)
        WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
            lambda d: "/new" not in d.current_url
        )
        log.info("  ✅ Created successfully: '%s'", loc_text)
        time.sleep(1)
        return True

    except Exception as e:
        log.error("  ❌ Failed for '%s': %s", loc_text, e)
        return False


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    driver = build_driver()
    success_list = []
    failed_list  = []

    try:
        login(driver)

        all_locations = get_all_locations(driver)
        if not all_locations:
            log.error("No locations found in dropdown. Exiting.")
            return

        to_process = all_locations if MAX_LOCATIONS == 0 else all_locations[:MAX_LOCATIONS]
        log.info("Will process %d / %d location(s).", len(to_process), len(all_locations))

        for idx, (loc_value, loc_text) in enumerate(to_process, 1):
            ok = create_mapping(driver, loc_value, loc_text, idx, len(to_process))
            (success_list if ok else failed_list).append(loc_text)

    except Exception as e:
        log.exception("Fatal error: %s", e)
    finally:
        print("\n" + "=" * 60)
        print("  VENDOR LOCATION MAPPING — SUMMARY")
        print("=" * 60)
        print(f"  Total     : {len(success_list) + len(failed_list)}")
        print(f"  ✅ Success : {len(success_list)}")
        print(f"  ❌ Failed  : {len(failed_list)}")
        if success_list:
            print("\n  Successful locations:")
            for loc in success_list:
                print(f"    ✅  {loc}")
        if failed_list:
            print("\n  Failed locations (retry manually):")
            for loc in failed_list:
                print(f"    ❌  {loc}")
        print("=" * 60)
        driver.quit()


if __name__ == "__main__":
    main()