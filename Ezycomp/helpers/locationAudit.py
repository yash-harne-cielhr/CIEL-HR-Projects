# =============================================================
#  Location Audit Workflow — Steps 1 + 2
#  Login → Select Role → Location Audits → Filters → Open Month
#  → Filter Audit Type → Edit each activity → Submit
# =============================================================

# ─────────────────────────────────────────────
#  GLOBAL CONFIGURATION  ← Edit these
# ─────────────────────────────────────────────

BASE_URL  = "https://ezycomp.ur-nl.com/"

USERNAME  = "ytestall"
PASSWORD  = "Ezycomp@1234"

# Role to switch to after login
# Options: "Vendor Admin" | "Vendor User" | "Auditor Admin" | "Auditor User" | "Client Admin"
TARGET_ROLE = "Vendor Admin"

# ── Filters ───────────────────────────────────
FILTER_COMPANY           = "CLRA Registers Management Pvt Ltd"
FILTER_ASSOCIATE_COMPANY = "CLRA Associates 2"
FILTER_LOCATION          = "Acropolis Mall - Kolkata, Kolkata"    # e.g. "City Center Mall Guwahati (AS-GUW-A2L0)" or "" for All
FILTER_TIME_RANGE        = "Full Year" # e.g. "Full Year" | "Monthly" | "Quarterly"
FILTER_YEAR              = "2025"      # e.g. "2025"

# ── Audit month to open ───────────────────────
# Must match exactly the text in the Month column, e.g. "December (2025)"
TARGET_AUDIT_MONTH = "September (2025)"

# ── Step 2: Activity processing ───────────────
# Audit Type filter inside the audit. Set "" to skip.
FILTER_audit_type = "Audit"

# Folder containing evidence files — a random file is picked each time
EVIDENCE_FOLDER = r"C:\Users\Yash Harne\OneDrive\Desktop\Upload File\1_Document\Less than 5 MB"

# 0.0–1.0 probability that an activity row is SKIPPED entirely (not edited)
SKIP_PROBABILITY = 0.2

# 0.0–1.0 probability that auditee remark is left BLANK (when not skipping)
BLANK_REMARK_PROBABILITY = 0.3

# 0.0–1.0 probability that evidence upload is SKIPPED (when not skipping)
BLANK_EVIDENCE_PROBABILITY = 0.3

# Auditee remark text used when not blank
AUDITEE_REMARK = "Audit completed and verified. All documents are in order."

HEADLESS          = False
PAGE_LOAD_TIMEOUT = 30
ELEMENT_WAIT      = 20

# ─────────────────────────────────────────────

import time
import random
import os
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


def wait_for(driver, by, selector, timeout=ELEMENT_WAIT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )


def wait_clickable(driver, by, selector, timeout=ELEMENT_WAIT):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )


def js_click(driver, el):
    """Click using JavaScript to bypass navbar/overlay interception."""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", el)


# ─────────────────────────────────────────────
#  REACT-SELECT HELPER
# ─────────────────────────────────────────────

def react_select(driver, input_id, search_text, exact=False, wait_ms=1800):
    """
    Interact with any react-select dropdown by its input element ID.
      1. JS-click the control to open
      2. Type search_text
      3. JS-click the first matching option
    Returns True on success.
    """
    log.info("    react-select[%s] → '%s'", input_id, search_text)
    try:
        input_el = WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.presence_of_element_located((By.ID, input_id))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", input_el)
        time.sleep(0.3)

        # Click the control container to open the dropdown
        try:
            control = input_el.find_element(
                By.XPATH,
                "./ancestor::div[contains(@class,'-control') or contains(@class,'__control')][1]"
            )
        except NoSuchElementException:
            control = input_el
        js_click(driver, control)
        time.sleep(0.5)

        # Clear + type
        input_el = driver.find_element(By.ID, input_id)
        input_el.send_keys(Keys.CONTROL + "a")
        input_el.send_keys(Keys.BACKSPACE)
        input_el.send_keys(search_text)
        time.sleep(wait_ms / 1000)

        # Wait for menu
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class*='-menu'], div[class*='__menu']")
                )
            )
        except TimeoutException:
            log.warning("    Menu slow — retrying open ...")
            js_click(driver, control)
            time.sleep(1)

        # Find and click the matching option
        opts = driver.find_elements(
            By.CSS_SELECTOR, "div[class*='-option'], div[class*='__option']"
        )
        search_lower = search_text.lower()
        for opt in opts:
            txt = opt.text.strip()
            if not txt:
                continue
            hit = (txt.lower() == search_lower) if exact else (search_lower in txt.lower())
            if hit:
                js_click(driver, opt)
                log.info("    ✅ Selected: '%s'", txt)
                time.sleep(0.8)
                return True

        available = [o.text.strip() for o in opts if o.text.strip()]
        log.error("    ❌ '%s' not found. Available: %s", search_text, available)
        try:
            driver.find_element(By.ID, input_id).send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return False

    except Exception as e:
        log.error("    react_select error [%s]: %s", input_id, e)
        return False


def react_select_by_label(driver, label_text, search_text, exact=False,
                           label_css="label", wait_ms=1800):
    """
    Find a react-select by its nearby label text, then call react_select().
    Tries multiple label CSS selectors for robustness.
    """
    log.info("    Finding react-select for label: '%s'", label_text)

    label_selectors = [
        label_css,
        "label.form-label",
        "label.filter-label",
        "label.form-label.text-sm",
        "label",
    ]

    for lbl_sel in label_selectors:
        try:
            labels = driver.find_elements(By.CSS_SELECTOR, lbl_sel)
            for lbl in labels:
                if label_text.lower() in lbl.text.strip().lower():
                    # Go up to a common container, find the react-select input inside
                    for ancestor_levels in range(1, 5):
                        xpath = "./parent::div" + "/parent::div" * (ancestor_levels - 1)
                        try:
                            container = lbl.find_element(By.XPATH, xpath)
                            inp = container.find_element(
                                By.CSS_SELECTOR, "input[id^='react-select'], input.audit-select__input"
                            )
                            input_id = inp.get_attribute("id")
                            if input_id:
                                return react_select(driver, input_id, search_text,
                                                    exact=exact, wait_ms=wait_ms)
                        except NoSuchElementException:
                            continue
        except Exception:
            continue

    log.error("    Could not find react-select for label '%s'.", label_text)
    return False


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────

def login(driver):
    log.info("Opening login page ...")
    driver.get(BASE_URL)
    time.sleep(2)

    # Username / email field
    username_field = WebDriverWait(driver, ELEMENT_WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
            "input[type='text'], input[type='email'], "
            "input[name='username'], input[name='email'], "
            "input[placeholder*='username' i], input[placeholder*='email' i]"
        ))
    )
    username_field.clear()
    username_field.send_keys(USERNAME)

    pwd_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    pwd_field.clear()
    pwd_field.send_keys(PASSWORD)

    login_btn = driver.find_element(By.CSS_SELECTOR,
        "button[type='submit'], input[type='submit'], button.btn-primary"
    )
    js_click(driver, login_btn)
    log.info("Login submitted.")

    # Wait for dashboard / navbar to appear
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        lambda d: "login" not in d.current_url.lower() and
                  len(d.find_elements(By.CSS_SELECTOR,
                      "nav, .sidenav, .sidebar, .navbar, .nav-link")) > 0
    )
    log.info("Login successful. URL: %s", driver.current_url)


# ─────────────────────────────────────────────
#  SWITCH ROLE
# ─────────────────────────────────────────────

def switch_role(driver, role_name):
    """
    Hover on the user display name (e.g. 'Ytest all roles') to open the
    role dropdown, then click the matching role option.
    """
    log.info("Switching role to: '%s' ...", role_name)

    # Find the user name element to hover on
    user_el = WebDriverWait(driver, ELEMENT_WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
            "div.fw-semibold.text-md, div[class*='fw-semibold'], "
            ".user-name, .nav-user, .dropdown-toggle"
        ))
    )
    # Hover using JS (simulate mouseenter)
    driver.execute_script("""
        var el = arguments[0];
        ['mouseover','mouseenter'].forEach(function(evt) {
            el.dispatchEvent(new MouseEvent(evt, {bubbles: true}));
        });
    """, user_el)
    time.sleep(0.8)

    # Also try a regular click to open the dropdown
    try:
        js_click(driver, user_el)
        time.sleep(0.5)
    except Exception:
        pass

    # Wait for dropdown menu items to appear
    try:
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                ".dropdown-menu, .dropdown-item, [class*='dropdown'] a, [role='menu']"
            ))
        )
    except TimeoutException:
        log.warning("Role dropdown did not appear — trying parent element ...")
        try:
            parent = user_el.find_element(By.XPATH, "./parent::div")
            js_click(driver, parent)
            time.sleep(0.8)
        except Exception:
            pass

    # Find and click the role option
    role_lower = role_name.lower()
    role_selectors = [
        ".dropdown-item",
        "[class*='dropdown'] a",
        "[role='menuitem']",
        "[role='option']",
        "a, button, div[class*='role'], li",
    ]

    for sel in role_selectors:
        try:
            items = driver.find_elements(By.CSS_SELECTOR, sel)
            for item in items:
                if role_lower in item.text.strip().lower() and item.is_displayed():
                    js_click(driver, item)
                    log.info("Role '%s' clicked.", item.text.strip())
                    time.sleep(2)
                    log.info("Role switched. URL: %s", driver.current_url)
                    return True
        except Exception:
            continue

    # Fallback: XPath text search
    try:
        role_el = driver.find_element(
            By.XPATH, f"//*[contains(text(),'{role_name}') and not(self::script)]"
        )
        if role_el.is_displayed():
            js_click(driver, role_el)
            log.info("Role '%s' selected via XPath.", role_name)
            time.sleep(2)
            return True
    except NoSuchElementException:
        pass

    log.error("Could not find role '%s' in dropdown.", role_name)
    return False


# ─────────────────────────────────────────────
#  NAVIGATE TO LOCATION AUDITS
# ─────────────────────────────────────────────

def go_to_location_audits(driver):
    log.info("Navigating to Location Audits ...")

    # Try clicking the sidebar nav link
    try:
        audit_link = WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/location-audits']"))
        )
        js_click(driver, audit_link)
        log.info("Clicked Location Audits nav link.")
    except TimeoutException:
        # Fallback: navigate directly
        log.warning("Nav link not found — navigating directly.")
        driver.get(BASE_URL.rstrip("/") + "/location-audits")

    # Wait for audit table / filter row to load
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        lambda d: "location-audits" in d.current_url and
                  len(d.find_elements(By.CSS_SELECTOR,
                      ".audit-filters-row, table, div[class*='audit']")) > 0
    )
    time.sleep(2)
    log.info("Location Audits page loaded.")


# ─────────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────────

def apply_filters(driver):
    """
    Apply all configured filters on the Location Audits page.
    The filter dropdowns use class 'audit-select__control' and input IDs
    like react-select-4-input (Company), react-select-5-input (Associate),
    react-select-6-input (Location), lal-time-range, lal-year.
    """
    log.info("Applying filters ...")

    # ── Company (react-select-4-input) ─────────────────────────────
    if FILTER_COMPANY:
        log.info("  Filter: Company = '%s'", FILTER_COMPANY)
        _apply_filter_by_label_or_id(driver, "Company", "react-select-4-input", FILTER_COMPANY)
        time.sleep(1.5)  # Let dependent dropdowns re-enable

    # ── Associate Company (react-select-5-input) ───────────────────
    if FILTER_ASSOCIATE_COMPANY:
        log.info("  Filter: Associate Company = '%s'", FILTER_ASSOCIATE_COMPANY)
        # Wait for Associate Company to become enabled after Company selection
        _wait_for_filter_enabled(driver, "react-select-5-input")
        _apply_filter_by_label_or_id(
            driver, "Associate Company", "react-select-5-input", FILTER_ASSOCIATE_COMPANY
        )
        time.sleep(1.5)

    # ── Location (react-select-6-input) ───────────────────────────
    if FILTER_LOCATION:
        log.info("  Filter: Location = '%s'", FILTER_LOCATION)
        _wait_for_filter_enabled(driver, "react-select-6-input")
        import re
        code_match = re.search(r'\(([^)]+)\)$', FILTER_LOCATION)
        search_key = code_match.group(1) if code_match else FILTER_LOCATION
        _apply_filter_by_label_or_id(driver, "Location", "react-select-6-input", search_key)
        time.sleep(1)
    else:
        log.info("  Filter: Location = All (skipped)")

    # ── Time Range (lal-time-range) ────────────────────────────────
    if FILTER_TIME_RANGE:
        log.info("  Filter: Time Range = '%s'", FILTER_TIME_RANGE)
        react_select(driver, "lal-time-range", FILTER_TIME_RANGE)
        time.sleep(1)

    # ── Year (lal-year) ────────────────────────────────────────────
    if FILTER_YEAR:
        log.info("  Filter: Year = '%s'", FILTER_YEAR)
        react_select(driver, "lal-year", FILTER_YEAR)
        time.sleep(1)

    log.info("All filters applied.")


def _apply_filter_by_label_or_id(driver, label_text, fallback_id, search_text):
    """Try label-based selection first; fall back to direct ID."""
    # Try known ID directly first (faster and more reliable)
    try:
        inp = driver.find_element(By.ID, fallback_id)
        if inp.is_displayed() and not inp.get_attribute("disabled"):
            react_select(driver, fallback_id, search_text, wait_ms=1800)
            return
    except NoSuchElementException:
        pass

    # Fallback: label search
    react_select_by_label(driver, label_text, search_text,
                           label_css="label.filter-label", wait_ms=1800)


def _wait_for_filter_enabled(driver, input_id, timeout=10):
    """Wait until a filter select input is no longer disabled."""
    log.info("    Waiting for filter input '%s' to become enabled ...", input_id)
    for _ in range(timeout):
        try:
            inp = driver.find_element(By.ID, input_id)
            if not inp.get_attribute("disabled"):
                log.info("    Filter input enabled.")
                return True
        except NoSuchElementException:
            pass
        time.sleep(1)
    log.warning("    Filter input '%s' still disabled after %ds.", input_id, timeout)
    return False


# ─────────────────────────────────────────────
#  OPEN AUDIT BY MONTH
# ─────────────────────────────────────────────

def open_audit_month(driver, month_text):
    """
    Find the row in the audit table whose Month column matches month_text
    and click it to open the audit.
    """
    log.info("Looking for audit month: '%s' ...", month_text)

    # Wait for the audit table to load
    WebDriverWait(driver, ELEMENT_WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table td, .audit-row, tr"))
    )
    time.sleep(1)

    month_lower = month_text.lower()

    # Strategy 1: find <td class="col-month"> matching the text
    try:
        tds = driver.find_elements(By.CSS_SELECTOR, "td.col-month, td[class*='month']")
        for td in tds:
            if month_lower in td.text.strip().lower():
                log.info("  Found month cell: '%s'", td.text.strip())
                # Click the row or the cell itself
                try:
                    row = td.find_element(By.XPATH, "./parent::tr")
                    js_click(driver, row)
                except Exception:
                    js_click(driver, td)
                time.sleep(2)
                log.info("  ✅ Audit opened for: '%s'", month_text)
                return True
    except Exception as e:
        log.warning("  col-month strategy failed: %s", e)

    # Strategy 2: any table cell containing the month text
    try:
        all_tds = driver.find_elements(By.CSS_SELECTOR, "td")
        for td in all_tds:
            if month_lower in td.text.strip().lower():
                log.info("  Found via general td: '%s'", td.text.strip())
                try:
                    row = td.find_element(By.XPATH, "./parent::tr")
                    js_click(driver, row)
                except Exception:
                    js_click(driver, td)
                time.sleep(2)
                log.info("  ✅ Audit opened for: '%s'", month_text)
                return True
    except Exception as e:
        log.warning("  General td strategy failed: %s", e)

    # Strategy 3: XPath text match
    try:
        el = driver.find_element(
            By.XPATH, f"//td[contains(text(),'{month_text}')]"
        )
        js_click(driver, el)
        time.sleep(2)
        log.info("  ✅ Audit opened via XPath for: '%s'", month_text)
        return True
    except NoSuchElementException:
        pass

    log.error("  ❌ Audit month '%s' not found in table.", month_text)

    # Debug: show what months are visible
    try:
        all_tds = driver.find_elements(By.CSS_SELECTOR, "td.col-month, td[class*='month']")
        visible = [td.text.strip() for td in all_tds if td.text.strip()]
        log.info("  Visible month cells: %s", visible)
    except Exception:
        pass

    return False


# ─────────────────────────────────────────────
#  STEP 2 HELPERS
# ─────────────────────────────────────────────

def get_random_evidence_file():
    """Return a random file path from EVIDENCE_FOLDER, or None if folder empty/missing."""
    try:
        if not os.path.isdir(EVIDENCE_FOLDER):
            log.warning("Evidence folder not found: %s", EVIDENCE_FOLDER)
            return None
        files = [
            os.path.join(EVIDENCE_FOLDER, f)
            for f in os.listdir(EVIDENCE_FOLDER)
            if os.path.isfile(os.path.join(EVIDENCE_FOLDER, f))
        ]
        if not files:
            log.warning("No files found in evidence folder.")
            return None
        chosen = random.choice(files)
        log.info("    Evidence file: %s", os.path.basename(chosen))
        return chosen
    except Exception as e:
        log.error("get_random_evidence_file error: %s", e)
        return None


def filter_audit_type(driver, audit_type):
    """Set the Audit Type filter inside the audit detail page."""
    if not audit_type:
        return
    log.info("  Filtering Audit Type: '%s' ...", audit_type)
    # Known input ID from HTML: react-select-22-input
    # Try direct ID first, fall back to label search
    try:
        inp = driver.find_element(By.ID, "react-select-22-input")
        react_select(driver, "react-select-22-input", audit_type, wait_ms=1500)
        time.sleep(1.5)
        return
    except NoSuchElementException:
        pass

    # Fallback: find by label "Activity" or "Audit Type"
    for label_text in ["Audit Type", "Audit"]:
        try:
            labels = driver.find_elements(By.CSS_SELECTOR, "label, .filter-label, small")
            for lbl in labels:
                if label_text.lower() in lbl.text.strip().lower():
                    container = lbl.find_element(By.XPATH,
                        "./parent::div/parent::div"
                    )
                    inp = container.find_element(
                        By.CSS_SELECTOR, "input[id^='react-select'], input.audit-select__input"
                    )
                    react_select(driver, inp.get_attribute("id"), audit_type, wait_ms=1500)
                    time.sleep(1.5)
                    return
        except Exception:
            continue
    log.warning("  Could not find Audit Type filter.")


def get_edit_buttons(driver):
    """Return all visible edit buttons on the activity list."""
    WebDriverWait(driver, ELEMENT_WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
            "button.al-icon-btn[title='Edit'], button[title='Edit']"
        ))
    )
    time.sleep(1)
    btns = driver.find_elements(By.CSS_SELECTOR,
        "button.al-icon-btn[title='Edit'], button[title='Edit']"
    )
    visible = [b for b in btns if b.is_displayed()]
    log.info("  Found %d edit button(s).", len(visible))
    return visible


def process_single_activity(driver, edit_btn_index, total):
    """
    Click the edit button at position edit_btn_index in the current list,
    fill remark + evidence randomly, and submit.
    Returns: "success" | "skipped" | "failed"
    """
    # Decide randomly whether to skip this activity
    if random.random() < SKIP_PROBABILITY:
        log.info("  [%d/%d] ⏭️  Randomly skipping this activity.", edit_btn_index + 1, total)
        return "skipped"

    try:
        # Re-fetch all edit buttons (DOM may have refreshed)
        btns = driver.find_elements(By.CSS_SELECTOR,
            "button.al-icon-btn[title='Edit'], button[title='Edit']"
        )
        visible = [b for b in btns if b.is_displayed()]

        if edit_btn_index >= len(visible):
            log.warning("  [%d/%d] Edit button index out of range (only %d visible).",
                        edit_btn_index + 1, total, len(visible))
            return "failed"

        btn = visible[edit_btn_index]
        log.info("  [%d/%d] Clicking Edit ...", edit_btn_index + 1, total)
        js_click(driver, btn)
        time.sleep(2)

        # ── Auditee Remark ─────────────────────────────────────────
        leave_remark_blank = random.random() < BLANK_REMARK_PROBABILITY
        try:
            remark_box = WebDriverWait(driver, ELEMENT_WAIT).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "textarea.ae-textarea, textarea[placeholder*='auditee' i]")
                )
            )
            if not leave_remark_blank:
                remark_box.clear()
                remark_box.send_keys(AUDITEE_REMARK)
                log.info("    Auditee remark filled.")
            else:
                log.info("    Auditee remark left blank (random).")
        except TimeoutException:
            log.warning("    Auditee remark textarea not found.")

        # ── Evidence Upload ────────────────────────────────────────
        leave_evidence_blank = random.random() < BLANK_EVIDENCE_PROBABILITY
        if not leave_evidence_blank:
            evidence_file = get_random_evidence_file()
            if evidence_file:
                try:
                    # Make the file input visible and send path
                    file_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "input[type='file']")
                        )
                    )
                    driver.execute_script(
                        "arguments[0].style.display='block';"
                        "arguments[0].style.visibility='visible';"
                        "arguments[0].style.opacity='1';",
                        file_input
                    )
                    time.sleep(0.3)
                    file_input.send_keys(evidence_file)
                    log.info("    Evidence uploaded: %s", os.path.basename(evidence_file))
                    time.sleep(1)
                except TimeoutException:
                    log.warning("    File input not found — skipping evidence.")
            else:
                log.warning("    No evidence file available — skipping upload.")
        else:
            log.info("    Evidence left blank (random).")

        # ── Submit ─────────────────────────────────────────────────
        submit_btn = WebDriverWait(driver, ELEMENT_WAIT).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.ae-submit, button[class*='ae-submit']")
            )
        )
        js_click(driver, submit_btn)
        log.info("    Submit clicked.")
        time.sleep(2.5)

        # Wait for the edit form to close (modal gone or list reloads)
        try:
            WebDriverWait(driver, 10).until(
                lambda d: len(d.find_elements(
                    By.CSS_SELECTOR, "textarea.ae-textarea"
                )) == 0 or
                len(d.find_elements(
                    By.CSS_SELECTOR, ".alert-success, .toast-success, .Toastify__toast--success"
                )) > 0
            )
        except TimeoutException:
            pass  # Continue even if we can't confirm close

        log.info("    ✅ Activity [%d/%d] submitted.", edit_btn_index + 1, total)
        time.sleep(1)
        return "success"

    except Exception as e:
        log.error("    ❌ Activity [%d/%d] failed: %s", edit_btn_index + 1, total, e)
        # Try to close any open form before continuing
        try:
            close = driver.find_element(By.CSS_SELECTOR,
                "button.btn-close, button[aria-label='Close'], .ae-cancel"
            )
            js_click(driver, close)
            time.sleep(1)
        except Exception:
            try:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(1)
            except Exception:
                pass
        return "failed"


def process_all_activities(driver):
    """
    Filter by Audit Type, then iterate through all edit buttons
    one by one, processing each activity.
    """
    log.info("=== Step 2: Processing activities ===")

    # Apply Audit Type filter
    filter_audit_type(driver, FILTER_audit_type)
    time.sleep(2)

    # Count total edit buttons
    try:
        btns = get_edit_buttons(driver)
        total = len(btns)
    except TimeoutException:
        log.error("No edit buttons found on the page.")
        return

    if total == 0:
        log.warning("No activities found to process.")
        return

    log.info("Processing %d activit(ies) ...", total)
    results = {"success": 0, "skipped": 0, "failed": 0}

    # Iterate by index — re-fetch list each time since DOM may refresh after submit
    for idx in range(total):
        log.info("--- Activity %d / %d ---", idx + 1, total)
        result = process_single_activity(driver, idx, total)
        results[result] += 1
        time.sleep(0.5)

    # Summary
    print("\n" + "=" * 55)
    print("  ACTIVITY PROCESSING SUMMARY")
    print("=" * 55)
    print(f"  Total activities : {total}")
    print(f"  ✅ Submitted     : {results['success']}")
    print(f"  ⏭️  Skipped       : {results['skipped']}")
    print(f"  ❌ Failed        : {results['failed']}")
    print("=" * 55 + "\n")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    driver = build_driver()

    try:
        # ── Step 1 ──────────────────────────────────────────────────
        login(driver)

        if not switch_role(driver, TARGET_ROLE):
            log.warning("Role switch may have failed — continuing anyway.")
        time.sleep(2)

        go_to_location_audits(driver)
        apply_filters(driver)
        time.sleep(1)

        opened = open_audit_month(driver, TARGET_AUDIT_MONTH)
        if not opened:
            log.error("Could not open audit '%s'. Exiting.", TARGET_AUDIT_MONTH)
            return

        log.info("✅ Audit '%s' opened. URL: %s", TARGET_AUDIT_MONTH, driver.current_url)
        time.sleep(2)

        # ── Step 2 ──────────────────────────────────────────────────
        process_all_activities(driver)

        log.info("Workflow complete.")
        input("\nPress Enter to close the browser ...")

    except Exception as e:
        log.exception("Fatal error: %s", e)
    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()