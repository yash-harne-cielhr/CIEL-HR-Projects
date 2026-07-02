# =============================================================
#  Location Vendor User Mapping
#  Frontend: https://ezycomp.ur-nl.com (React app)
#  All dropdowns are react-select — click + type + select option
# =============================================================

# ─────────────────────────────────────────────
#  GLOBAL CONFIGURATION
# ─────────────────────────────────────────────

LOGIN_URL    = "https://ezycomp.ur-nl.com/"
MAPPING_PATH = "/userManagement/location-vendor-mapping"

EMAIL    = "yash.harne@cielhr.com"
PASSWORD = "Ezycomp@1234"

TARGET_USER            = "Ytest all roles"
TARGET_COMPANY         = "CLRA Registers Management Pvt Ltd"
TARGET_ASSOCIATE       = "CLRA Associates 2"
TARGET_VENDOR_CATEGORY = "Security Services"
TARGET_VENDOR          = "CLRA Vendor 1"

# 0 = all 68 locations; set to e.g. 3 to test with first 3 only
MAX_LOCATIONS = 0

HEADLESS          = False
PAGE_LOAD_TIMEOUT = 30
ELEMENT_WAIT      = 20

# ── All 68 locations (already confirmed from your log) ────────
ALL_LOCATIONS = [
    'City Center Mall Guwahati (AS-GUW-A2L0)',
    'City Center Mall - Patna (BH-PAT-A2L1)',
    'Caculo Mall - Goa (GA-PNJ-A2L6)',
    'Maruti Solaris Mall (GJ-VAD-A2L8)',
    'Palladium Mall Ahmedabad (GJ-AHD-A2L9)',
    'VR Mall Surat (GJ-SURAT-A2M0)',
    'MGF Metropolitan Mall (HR-AMBALA-A2M2)',
    'Phoenix Market City Mall - Bangalore (KA-BG-A2M4)',
    'Orion Mall - Bangalore (KA-BG-A2M5)',
    'Nexus Koramangla - Bangalore (KA-BG-A2M7)',
    'Mall of Asia Bangalore (KA-BG-A2N0)',
    'Inorbit Mall - Hubli (KA-HUBLI-A2N2)',
    'Hilite Mall - Kozhikode (KL-KOZ-A2N3)',
    'DB City Mall Bhopal (MP-BHO-A2N5)',
    'Pavillion Mall - Pune (MH-PNC-A2N6)',
    'Phoenix Market City Mall - Pune (MH-PNC-A2N8)',
    'Phoenix Mall of the Millennium Pune (MH-PNC-A2N9)',
    'Palladium Mall Lower Parel (MH-MB-A2O0)',
    'Regional Office West (MH-BHI-A2O2)',
    'The Capital - Vasai (MH-MB-A2O5)',
    'Market City - Kurla (MH-MB-A2O7)',
    'Oberoi Mall Goregon (MH-MB-A2O8)',
    'Inorbit Mall - Malad (MH-MB-A2P0)',
    'Orion Mall - Panvel (MH-PNV-A2P1)',
    'Xperia Mall - Dombivali (MH-MB-A2P2)',
    'VR Mall (MH-VAS-A2P4)',
    'Utkal Galleria Mall (OD-ROU-A2P6)',
    'Plutone mall Rourkela (OD-ROU-A2P7)',
    'Pavilion Mall Ludhiana (PJ-LUD-A2P9)',
    'Mall of Amritsar (PJ-AMR-A2Q0)',
    'VR Mall - Chennai (TN-CH-A2Q2)',
    'The Marina Mall - Chennai (TN-CH-A2Q3)',
    'Express Avenue - Chennai (TN-CH-A2Q5)',
    'Sarath City Mall Play N Learn (TL-HYD-A2Q6)',
    'Phoenix United Bareilly (UP-BAREILLY-A2Q9)',
    'Logix City Centre Mall (UP-JHANSI-A2R0)',
    'Phoenix Palassio (UP-JHANSI-A2R1)',
    'Gaur City Mall - Noida (UP-NOI-A2R2)',
    'South City Mall - Kolkata (WB-KL-A2R3)',
    'Acropolis Mall - Kolkata (WB-KL-A2R4)',
    'City Centre Mall - Siliguri (WB-SIL-A2R5)',
    'City Centre Mall - Kolkata (WB-KL-A2R6)',
    'Diamond City North Mall - Kolkata (WB-KL-A2R7)',
    'Inorbit Mall Hyderabad PL (TL-HYD-A2Q7)',
    'GVK One Mall - Hyderabad (TL-HYD-A2Q8)',
    'Palladium Mall - Chennai (TN-CH-A2Q4)',
    'Celebration Mall - Udaipur (RJ-UDA-A2Q1)',
    'Esplanade One - Bhubaneswar (OD-BHU-A2P8)',
    'City Centre Mall - Nashik (MH-NASHIK-A2P5)',
    'Inorbit Mall - Vashi (MH-VAS-A2P3)',
    'Korum Mall - Thane (MH-TH-A2O9)',
    'Warehouse (MH-MB-A2O6)',
    'Seasons Mall - Pune (MH-PNC-A2O4)',
    'Support Office (MH-BHI-A2O3)',
    'R City Mall(FEC) - Ghatkopar NEW (MH-MB-A2O1)',
    'R-Mall - Thane (MH-TH-A2N7)',
    'Phoenix Citadel Mall Indore (MP-IND-A2N4)',
    'Mantri Square Mall \u2013 Bangalore (KA-BG-A2N1)',
    'Regional Office - South (KA-MYR-A2M9)',
    'Nexus Fiza Mall - Mangalore (KA-MAG-A2M8)',
    'Nexus Shantiniketan Mall Bangalore (KA-BG-A2M6)',
    'Ambience Mall (HR-AMBALA-A2M3)',
    'Regional Office - North (HR-AMBALA-A2M1)',
    'Inorbit Mall - Vadodara (GJ-VAD-A2L7)',
    'Ambience Mall Vasant Kunj (DL-FARIDABAD-A2L5)',
    'Pacific Mall - Delhi (DL-DEL-A2L4)',
    'Vegas Mall - Delhi (DL-DEL-A2L3)',
    'Magneto - Raipur (CH-RP-A2L2)',
]

# ─────────────────────────────────────────────

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, StaleElementReferenceException
)

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
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
    else:
        driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver


# ─────────────────────────────────────────────
#  REACT-SELECT HELPER
# ─────────────────────────────────────────────

def react_select_by_label(driver, label_text, search_text, exact=False):
    """
    Find a react-select by its <label> text, open it, type to filter,
    and click the matching option.
    Uses JS click to avoid interception by navbar/overlays.
    """
    log.info("    [react-select] label='%s'  search='%s'", label_text, search_text)

    # Find the label and get its sibling input
    try:
        labels = driver.find_elements(By.CSS_SELECTOR, "label.form-label, label.form-label.text-sm")
        input_el = None
        for lbl in labels:
            if label_text.lower() in lbl.text.strip().lower():
                form_group = lbl.find_element(By.XPATH, "./parent::div")
                input_el = form_group.find_element(
                    By.CSS_SELECTOR, "input[id^='react-select']"
                )
                break

        if input_el is None:
            log.error("    Label '%s' not found on page.", label_text)
            return False

        input_id = input_el.get_attribute("id")

        # Scroll into view and click the control using JS (avoids navbar interception)
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", input_el)
        time.sleep(0.3)

        control = input_el.find_element(
            By.XPATH, "./ancestor::div[contains(@class,'-control')][1]"
        )
        driver.execute_script("arguments[0].click();", control)
        time.sleep(0.5)

        # Clear any existing text and type the search
        input_el = driver.find_element(By.ID, input_id)  # re-fetch after click
        input_el.send_keys(Keys.CONTROL + "a")
        input_el.send_keys(Keys.BACKSPACE)
        # Type the search text character by character for reliability
        input_el.send_keys(search_text)
        time.sleep(1.8)  # Wait for AJAX filter

        # Wait for menu to appear
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='-menu']"))
            )
        except TimeoutException:
            log.warning("    Dropdown menu did not appear — retrying click ...")
            driver.execute_script("arguments[0].click();", control)
            time.sleep(1)

        # Get all visible options
        options = driver.find_elements(By.CSS_SELECTOR, "div[class*='-option']")
        if not options:
            log.error("    No options found in dropdown for '%s'.", search_text)
            input_el.send_keys(Keys.ESCAPE)
            return False

        search_lower = search_text.lower()
        for opt in options:
            opt_text = opt.text.strip()
            if not opt_text:
                continue
            match = (opt_text.lower() == search_lower) if exact else (search_lower in opt_text.lower())
            if match:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", opt)
                    driver.execute_script("arguments[0].click();", opt)  # JS click — avoids overlay
                    log.info("    ✅ Selected: '%s'", opt_text)
                    time.sleep(0.8)
                    return True
                except StaleElementReferenceException:
                    # Re-fetch and retry once
                    time.sleep(0.5)
                    opts2 = driver.find_elements(By.CSS_SELECTOR, "div[class*='-option']")
                    for o2 in opts2:
                        if search_lower in o2.text.strip().lower():
                            driver.execute_script("arguments[0].click();", o2)
                            log.info("    ✅ Selected (retry): '%s'", o2.text.strip())
                            time.sleep(0.8)
                            return True

        available = [o.text.strip() for o in options if o.text.strip()]
        log.error("    ❌ '%s' not found. Available: %s", search_text, available)
        # Close dropdown
        try:
            input_el = driver.find_element(By.ID, input_id)
            input_el.send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return False

    except Exception as e:
        log.error("    react_select_by_label error for '%s': %s", label_text, e)
        return False


# ─────────────────────────────────────────────
#  CLOSE DIALOG — always use JS click
# ─────────────────────────────────────────────

def close_dialog(driver):
    """Close modal using JS click to avoid navbar interception."""
    try:
        close_btn = driver.find_element(
            By.CSS_SELECTOR, "button.btn-close, button[aria-label='Close']"
        )
        driver.execute_script("arguments[0].click();", close_btn)
        log.info("    Dialog closed via JS click.")
        time.sleep(1)
        return True
    except NoSuchElementException:
        pass

    # Fallback: Escape key
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        log.info("    Dialog closed via Escape.")
        time.sleep(1)
        return True
    except Exception:
        pass

    return False


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────

def login(driver):
    log.info("Navigating to login page ...")
    driver.get(LOGIN_URL)
    time.sleep(2)

    email_field = WebDriverWait(driver, ELEMENT_WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
            "input[type='email'], input[name='email'], input[placeholder*='email' i], input[placeholder*='username' i]"
        ))
    )
    email_field.clear()
    email_field.send_keys(EMAIL)

    pwd_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    pwd_field.clear()
    pwd_field.send_keys(PASSWORD)

    login_btn = driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], button.btn-primary"
    )
    login_btn.click()
    log.info("Login submitted.")

    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        lambda d: "login" not in d.current_url.lower() and
                  len(d.find_elements(By.CSS_SELECTOR, "nav, .sidenav, .sidebar, .navbar")) > 0
    )
    log.info("Login successful.")


# ─────────────────────────────────────────────
#  NAVIGATE TO PAGE
# ─────────────────────────────────────────────

def go_to_mapping_page(driver):
    url = LOGIN_URL.rstrip("/") + MAPPING_PATH
    log.info("Navigating to: %s", url)
    driver.get(url)
    time.sleep(3)
    WebDriverWait(driver, ELEMENT_WAIT).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "input[id^='react-select']")) > 0
    )
    log.info("Mapping page loaded.")


# ─────────────────────────────────────────────
#  SELECT USER
# ─────────────────────────────────────────────

def react_select_by_input_id(driver, input_id, search_text):
    """
    Directly target a react-select by its input element ID.
    Same logic as react_select_by_label but skips the label-finding step.
    """
    log.info("    [react-select] input_id='%s'  search='%s'", input_id, search_text)
    try:
        input_el = WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.presence_of_element_located((By.ID, input_id))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", input_el)
        time.sleep(0.3)

        control = input_el.find_element(
            By.XPATH, "./ancestor::div[contains(@class,'-control')][1]"
        )
        driver.execute_script("arguments[0].click();", control)
        time.sleep(0.5)

        input_el = driver.find_element(By.ID, input_id)
        input_el.send_keys(Keys.CONTROL + "a")
        input_el.send_keys(Keys.BACKSPACE)
        input_el.send_keys(search_text)
        time.sleep(1.8)

        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='-menu']"))
            )
        except TimeoutException:
            log.warning("    Menu did not appear, retrying click ...")
            driver.execute_script("arguments[0].click();", control)
            time.sleep(1)

        options = driver.find_elements(By.CSS_SELECTOR, "div[class*='-option']")
        search_lower = search_text.lower()
        for opt in options:
            opt_text = opt.text.strip()
            if search_lower in opt_text.lower():
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", opt)
                driver.execute_script("arguments[0].click();", opt)
                log.info("    ✅ Selected: '%s'", opt_text)
                time.sleep(0.8)
                return True

        available = [o.text.strip() for o in options if o.text.strip()]
        log.error("    ❌ '%s' not found. Available: %s", search_text, available)
        input_el = driver.find_element(By.ID, input_id)
        input_el.send_keys(Keys.ESCAPE)
        return False

    except Exception as e:
        log.error("    react_select_by_input_id error: %s", e)
        return False


def select_user(driver):
    log.info("Selecting user: '%s' ...", TARGET_USER)

    # Wait for page to fully render react-select inputs
    WebDriverWait(driver, ELEMENT_WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[id^='react-select']"))
    )
    time.sleep(1)

    # Strategy 1: try known ID "react-select-2-input" (from original HTML)
    try:
        el = driver.find_element(By.ID, "react-select-2-input")
        if el.is_displayed():
            log.info("  Using react-select-2-input")
            return react_select_by_input_id(driver, "react-select-2-input", TARGET_USER)
    except NoSuchElementException:
        pass

    # Strategy 2: find all react-select inputs on the page and try the first visible one
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[id^='react-select']")
    log.info("  Found %d react-select inputs on page.", len(inputs))
    for inp in inputs:
        if inp.is_displayed():
            input_id = inp.get_attribute("id")
            log.info("  Trying input: %s", input_id)
            result = react_select_by_input_id(driver, input_id, TARGET_USER)
            if result:
                return True

    # Strategy 3: label-based search as last resort
    log.info("  Trying label-based search ...")
    return react_select_by_label(driver, "User", TARGET_USER)


# ─────────────────────────────────────────────
#  ADD ONE VENDOR MAPPING
# ─────────────────────────────────────────────

def add_vendor_mapping(driver, location_name, index, total):
    """Open Add Vendor dialog, fill all fields, submit. Returns True on success."""
    log.info("=== [%d/%d] Location: '%s' ===", index, total, location_name)

    try:
        # ── Open Add Vendor dialog ──────────────────────────────────
        add_btn = WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Vendor')]"))
        )
        driver.execute_script("arguments[0].click();", add_btn)
        time.sleep(2)
        log.info("  Add Vendor dialog opened.")

        # ── 1. Company ──────────────────────────────────────────────
        log.info("  [1/5] Company ...")
        if not react_select_by_label(driver, "Company", TARGET_COMPANY):
            log.error("  ❌ Company failed.")
            close_dialog(driver)
            return False
        time.sleep(1)

        # ── 2. Associate Company ────────────────────────────────────
        log.info("  [2/5] Associate Company ...")
        if not react_select_by_label(driver, "Associate Company", TARGET_ASSOCIATE):
            log.error("  ❌ Associate Company failed.")
            close_dialog(driver)
            return False
        time.sleep(1.5)

        # ── 3. Location ─────────────────────────────────────────────
        log.info("  [3/5] Location: '%s' ...", location_name)
        # Use the location code (text inside parentheses) as search key
        # e.g. "City Center Mall Guwahati (AS-GUW-A2L0)" → search "AS-GUW-A2L0"
        # This is short and unique — avoids ambiguity with long names
        import re
        code_match = re.search(r'\(([^)]+)\)$', location_name)
        search_key = code_match.group(1) if code_match else location_name

        if not react_select_by_label(driver, "Location", search_key):
            # Fallback: try full name
            log.warning("  Code search failed, trying full name ...")
            if not react_select_by_label(driver, "Location", location_name):
                log.error("  ❌ Location failed.")
                close_dialog(driver)
                return False
        time.sleep(1)

        # ── 4. Vendor Category ──────────────────────────────────────
        log.info("  [4/5] Vendor Category ...")
        if not react_select_by_label(driver, "Vendor Category", TARGET_VENDOR_CATEGORY):
            log.error("  ❌ Vendor Category failed.")
            close_dialog(driver)
            return False
        time.sleep(1.5)

        # ── 5. Select CLRA Vendor 1 from the vendor list ───────────
        log.info("  [5/5] Selecting vendor '%s' from list ...", TARGET_VENDOR)
        if not select_vendor_from_list(driver, TARGET_VENDOR):
            log.error("  ❌ Vendor selection failed.")
            close_dialog(driver)
            return False
        time.sleep(0.5)

        # ── Submit ──────────────────────────────────────────────────
        log.info("  Submitting ...")
        submit_btn = WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "button[type='submit'], .modal-footer button.btn-primary"
            ))
        )
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(2.5)

        # Confirm modal closed (success)
        WebDriverWait(driver, ELEMENT_WAIT).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, ".modal.show")) == 0 or
                      len(d.find_elements(By.CSS_SELECTOR,
                          ".alert-success, .toast-success, .Toastify__toast--success"
                      )) > 0
        )
        log.info("  ✅ Created: '%s'", location_name)
        time.sleep(1)
        return True

    except Exception as e:
        log.error("  ❌ Error for '%s': %s", location_name, e)
        close_dialog(driver)
        return False


# ─────────────────────────────────────────────
#  SELECT VENDOR FROM LIST (after Vendor Category chosen)
# ─────────────────────────────────────────────

def select_vendor_from_list(driver, vendor_name):
    """
    After selecting Vendor Category, a vendor list appears.
    Find the row/item matching vendor_name and click it.
    Tries multiple selectors.
    """
    vendor_lower = vendor_name.lower()
    time.sleep(1)  # Wait for vendor list to render

    # Strategy 1: table rows / list items containing the vendor name
    xpaths = [
        f"//td[normalize-space(text())='{vendor_name}']",
        f"//td[contains(text(),'{vendor_name}')]",
        f"//li[contains(text(),'{vendor_name}')]",
        f"//span[contains(text(),'{vendor_name}')]",
        f"//div[contains(@class,'vendor') and contains(.,'{vendor_name}')]",
        f"//*[contains(@class,'locationsList') or contains(@class,'vendor-list')]//*[contains(.,'{vendor_name}')]",
    ]

    for xpath in xpaths:
        try:
            els = driver.find_elements(By.XPATH, xpath)
            for el in els:
                if vendor_lower in el.text.strip().lower() and el.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    driver.execute_script("arguments[0].click();", el)
                    log.info("    ✅ Vendor selected via xpath: '%s'", el.text.strip())
                    time.sleep(0.5)
                    return True
        except Exception:
            continue

    # Strategy 2: any visible element whose text matches exactly
    try:
        all_els = driver.find_elements(By.XPATH, f"//*[contains(text(),'{vendor_name}')]")
        for el in all_els:
            if el.is_displayed() and vendor_lower in el.text.strip().lower():
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                driver.execute_script("arguments[0].click();", el)
                log.info("    ✅ Vendor selected via text scan: '%s'", el.text.strip())
                time.sleep(0.5)
                return True
    except Exception as e:
        log.warning("    Text scan failed: %s", e)

    log.error("    ❌ Could not find vendor '%s' in list.", vendor_name)
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
        go_to_mapping_page(driver)

        # Select user once — stays for all mappings
        if not select_user(driver):
            log.error("Could not select user '%s'. Exiting.", TARGET_USER)
            return
        time.sleep(2)

        to_process = ALL_LOCATIONS if MAX_LOCATIONS == 0 else ALL_LOCATIONS[:MAX_LOCATIONS]
        log.info("Processing %d / %d location(s).", len(to_process), len(ALL_LOCATIONS))

        for idx, location in enumerate(to_process, 1):
            ok = add_vendor_mapping(driver, location, idx, len(to_process))
            (success_list if ok else failed_list).append(location)

    except Exception as e:
        log.exception("Fatal error: %s", e)
    finally:
        print("\n" + "=" * 62)
        print("  VENDOR USER MAPPING — SUMMARY REPORT")
        print("=" * 62)
        print(f"  User      : {TARGET_USER}")
        print(f"  Total     : {len(success_list) + len(failed_list)}")
        print(f"  ✅ Success : {len(success_list)}")
        print(f"  ❌ Failed  : {len(failed_list)}")
        if success_list:
            print("\n  Successful:")
            for loc in success_list:
                print(f"    ✅  {loc}")
        if failed_list:
            print("\n  Failed (retry manually):")
            for loc in failed_list:
                print(f"    ❌  {loc}")
        print("=" * 62)
        driver.quit()


if __name__ == "__main__":
    main()