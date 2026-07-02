# Gmail Email Validator - attaches to an ALREADY RUNNING Chrome instance.
#
# SETUP (do this ONCE before running the script):
# ------------------------------------------------
# 1. Close all Chrome windows completely.
# 2. Launch Chrome manually with remote debugging enabled:
#
#    Windows (run in CMD or PowerShell):
#    "C:/Program Files/Google/Chrome/Application/chrome.exe" --remote-debugging-port=9222
#       --user-data-dir="C:/Users/Yash Harne/AppData/Local/Google/Chrome/User Data"
#       --profile-directory="Default"
#
#    Mac:
#    /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --remote-debugging-port=9222
#
#    Linux:
#    google-chrome --remote-debugging-port=9222
#
# 3. In that Chrome window, open Gmail and make sure you are logged in.
# 4. Run this script - it will attach to that Chrome window.

# ─────────────────────────────────────────────
#  GLOBAL CONFIGURATION
# ─────────────────────────────────────────────

DEBUGGER_ADDRESS    = "localhost:9222"   # Must match --remote-debugging-port above

SUBJECT_KEYWORDS    = "Employee Wage Upload Completed Successfully"

WAIT_TIMEOUT        = 30    # Seconds to wait for page elements
CHECK_INBOX_ONLY    = True  # True = search only Inbox; False = search all mail
MAX_EMAILS_TO_SCAN  = 20    # How many result rows to scan (0 = all visible)

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
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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
#  DRIVER — attach to existing Chrome
# ─────────────────────────────────────────────

def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_experimental_option("debuggerAddress", DEBUGGER_ADDRESS)

    if USE_DRIVER_MANAGER:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(WAIT_TIMEOUT)
    log.info("Attached to existing Chrome at %s", DEBUGGER_ADDRESS)
    log.info("Current tab: %s", driver.current_url)
    return driver


def wait_for(driver, by, selector, timeout=WAIT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )

def wait_clickable(driver, by, selector, timeout=WAIT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )


# ─────────────────────────────────────────────
#  OPEN GMAIL TAB
# ─────────────────────────────────────────────

def open_gmail(driver: webdriver.Chrome) -> None:
    """Navigate to Gmail inbox (reuses the logged-in session in the open Chrome)."""
    log.info("Navigating to Gmail inbox …")
    driver.get("https://mail.google.com/mail/u/0/#inbox")
    time.sleep(3)

    if "accounts.google.com" in driver.current_url:
        raise RuntimeError(
            "Gmail is asking for login — you are not logged in on this Chrome window.\n"
            "Please log into Gmail manually in the Chrome window you launched, then re-run."
        )
    log.info("Gmail inbox loaded successfully.")


# ─────────────────────────────────────────────
#  SEARCH
# ─────────────────────────────────────────────

def search_email_by_subject(driver: webdriver.Chrome, subject: str) -> bool:
    log.info("Searching for subject: '%s'", subject)

    search_query = f'subject:"{subject}"'
    if CHECK_INBOX_ONLY:
        search_query = f'in:inbox {search_query}'

    try:
        search_box = wait_clickable(driver, By.CSS_SELECTOR, "input[aria-label='Search mail']")
    except TimeoutException:
        search_box = wait_clickable(driver, By.CSS_SELECTOR, "input[name='q']")

    search_box.clear()
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    log.info("Search submitted.")
    time.sleep(3)

    return parse_search_results(driver, subject)


# ─────────────────────────────────────────────
#  PARSE RESULTS
# ─────────────────────────────────────────────

def parse_search_results(driver: webdriver.Chrome, subject_keyword: str) -> bool:
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.zA"))
        )
    except TimeoutException:
        log.warning("No email rows found for this search query.")
        return False

    rows = driver.find_elements(By.CSS_SELECTOR, "tr.zA")
    total = len(rows)
    log.info("Found %d email row(s) in search results.", total)

    scan_limit = MAX_EMAILS_TO_SCAN if MAX_EMAILS_TO_SCAN > 0 else total
    keyword_lower = subject_keyword.lower()

    for idx, row in enumerate(rows[:scan_limit]):
        subject_text = ""
        try:
            subject_text = row.find_element(By.CSS_SELECTOR, "span.bog").text.strip()
        except NoSuchElementException:
            pass

        log.info("[%d/%d] Subject: '%s'", idx + 1, scan_limit, subject_text)

        if keyword_lower in subject_text.lower():
            log.info("✅  MATCH FOUND at row %d — '%s'", idx + 1, subject_text)
            return True

    log.info("❌  No matching email found in %d scanned result(s).", min(scan_limit, total))
    return False


# ─────────────────────────────────────────────
#  OPEN EMAIL & EXTRACT DETAILS
# ─────────────────────────────────────────────

def open_and_validate_email(driver: webdriver.Chrome, subject_keyword: str) -> dict:
    result = {"found": False, "subject": None, "sender": None, "date": None, "body_snippet": None}

    try:
        rows = driver.find_elements(By.CSS_SELECTOR, "tr.zA")
        keyword_lower = subject_keyword.lower()

        for row in rows:
            subject_text = ""
            try:
                subject_text = row.find_element(By.CSS_SELECTOR, "span.bog").text.strip()
            except NoSuchElementException:
                pass

            if keyword_lower not in subject_text.lower():
                continue

            result["subject"] = subject_text

            try:
                sender_el = row.find_element(By.CSS_SELECTOR, "span.zF")
                result["sender"] = sender_el.get_attribute("name") or sender_el.text.strip()
            except NoSuchElementException:
                pass

            try:
                date_el = row.find_element(By.CSS_SELECTOR, "td.xW span")
                result["date"] = date_el.get_attribute("title") or date_el.text.strip()
            except NoSuchElementException:
                pass

            row.click()
            time.sleep(3)

            try:
                body_el = WebDriverWait(driver, WAIT_TIMEOUT).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.a3s.aiL, div.gs div[data-message-id]")
                    )
                )
                result["body_snippet"] = body_el.text[:500]
            except TimeoutException:
                result["body_snippet"] = "(Could not extract body)"

            result["found"] = True
            break

    except Exception as exc:
        log.warning("Error while opening email: %s", exc)

    return result


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main() -> None:
    chrome_cmd = (
        r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
        r' --remote-debugging-port=9222'
        r' --user-data-dir="C:\Users\Yash Harne\AppData\Local\Google\Chrome\User Data"'
        r' --profile-directory="Default"'
    )
    print("\n" + "=" * 62)
    print("  PRE-RUN CHECKLIST")
    print("=" * 62)
    print("  1. Launch Chrome with this command (CMD / PowerShell):\n")
    print(f"     {chrome_cmd}\n")
    print("  2. Log into Gmail in that Chrome window.")
    print("  3. Then run this script.")
    print("=" * 62 + "\n")

    driver = build_driver()

    try:
        open_gmail(driver)

        found = search_email_by_subject(driver, SUBJECT_KEYWORDS)

        if found:
            details = open_and_validate_email(driver, SUBJECT_KEYWORDS)
            print("\n" + "=" * 60)
            print("  EMAIL VALIDATION REPORT")
            print("=" * 60)
            print(f"  Status      : ✅  FOUND")
            print(f"  Subject     : {details['subject']}")
            print(f"  Sender      : {details['sender']}")
            print(f"  Date        : {details['date']}")
            print(f"  Body Snippet:\n  {details['body_snippet']}")
            print("=" * 60 + "\n")
        else:
            print("\n" + "=" * 60)
            print("  EMAIL VALIDATION REPORT")
            print("=" * 60)
            print(f"  Status   : ❌  NOT FOUND")
            print(f"  Searched : {SUBJECT_KEYWORDS}")
            print("=" * 60 + "\n")

    except RuntimeError as e:
        log.error(str(e))
    except Exception as exc:
        log.exception("Unexpected error: %s", exc)
    # NOTE: We do NOT call driver.quit() here — that would close your Chrome window!
    finally:
        log.info("Script finished. Chrome window left open.")


if __name__ == "__main__":
    main()