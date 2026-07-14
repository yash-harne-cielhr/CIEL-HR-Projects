# =============================================================
# Audit Replication Automation
# Part 1 - Configuration + Driver + React Select Helper
# =============================================================

import logging
import re
import time
from dataclasses import dataclass
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WDM = True
except ImportError:
    USE_WDM = False


# =============================================================
# CONFIGURATION
# =============================================================

LOGIN_URL = "https://ezycomp.ur-nl.com/"
AUDIT_URL = "https://ezycomp.ur-nl.com/auditSchedule/details"

USERNAME = "your_username"
PASSWORD = "your_password"

SOURCE_COMPANY = "CLRA Registers Management Pvt Ltd"
SOURCE_ASSOCIATE = "CLRA Associates 2"
SOURCE_LOCATION = "City Center Mall Guwahati"

SOURCE_MONTH = "January"
SOURCE_YEAR = "2025"

DEST_COMPANY = "CLRA Registers Management Pvt Ltd"
DEST_ASSOCIATE = "CLRA Associates 2"

DEST_MONTHS = [
    "Mar 2026",
    "Apr 2026",
    "May 2026",
]

DEST_SKIP_LOCATIONS = []

HEADLESS = False

PAGE_TIMEOUT = 30
WAIT = 20


# =============================================================
# LOGGING
# =============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)

log = logging.getLogger("AuditReplication")


# =============================================================
# MONTHS
# =============================================================

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

MONTH_MAP = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December",
}


# =============================================================
# DRIVER
# =============================================================

def build_driver():

    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    if USE_WDM:

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options
        )

    else:

        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(PAGE_TIMEOUT)

    return driver


# =============================================================
# COMMON HELPERS
# =============================================================

class Common:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT)

    # ---------------------------------------------------------

    def sleep(self, sec=1):

        time.sleep(sec)

    # ---------------------------------------------------------

    def scroll(self, element):

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block:'center'
            });
            """,
            element,
        )

    # ---------------------------------------------------------

    def js_click(self, element):

        self.scroll(element)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    # ---------------------------------------------------------

    def visible(self, locator):

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    # ---------------------------------------------------------

    def present(self, locator):

        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    # ---------------------------------------------------------

    def clickable(self, locator):

        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    # ---------------------------------------------------------

    def exists(self, locator):

        try:

            self.driver.find_element(*locator)

            return True

        except:

            return False

    # ---------------------------------------------------------

    def retry(self, fn, attempts=3):

        last = None

        for _ in range(attempts):

            try:

                return fn()

            except Exception as e:

                last = e

                self.sleep(0.5)

        raise last


# =============================================================
# REACT SELECT
# =============================================================

class ReactSelect:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT)
        self.common = Common(driver)

    # ---------------------------------------------------------

    def _container(self, label):

        xpath = (
            f"//label[.//small[normalize-space()='{label}']]"
            "/following-sibling::div"
        )

        return self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)
            )
        )

    # ---------------------------------------------------------

    def _input(self, label):

        container = self._container(label)

        return container.find_element(
            By.CSS_SELECTOR,
            "input[id^='react-select']"
        )

    # ---------------------------------------------------------

    def _control(self, label):

        container = self._container(label)

        return container.find_element(
            By.CSS_SELECTOR,
            "div[class*='control']"
        )

    # ---------------------------------------------------------

    def open(self, label):

        control = self._control(label)

        self.common.js_click(control)

        self.common.sleep(0.4)

    # ---------------------------------------------------------

    def clear(self, label):

        inp = self._input(label)

        inp.send_keys(Keys.CONTROL + "a")

        inp.send_keys(Keys.DELETE)

    # ---------------------------------------------------------

    def type(self, label, text):

        inp = self._input(label)

        inp.send_keys(text)

        self.common.sleep(0.8)

    # ---------------------------------------------------------

    def options(self):

        return self.driver.find_elements(
            By.CSS_SELECTOR,
            "div[class*='option']"
        )

    # ---------------------------------------------------------

    def choose(self, text):

        options = self.wait.until(
            lambda d: [
                x
                for x in self.options()
                if x.is_displayed()
            ]
        )

        text = text.lower()

        for option in options:

            value = option.text.strip().lower()

            if value == text:

                self.common.js_click(option)

                return

        for option in options:

            value = option.text.strip().lower()

            if text in value:

                self.common.js_click(option)

                return

        raise Exception(
            f"Option '{text}' not found."
        )

    # ---------------------------------------------------------

    def select(self, label, value):

        log.info(f"{label} -> {value}")

        def work():

            self.open(label)

            self.clear(label)

            self.type(label, value)

            self.choose(value)

        self.common.retry(work)

# =============================================================
# LOGIN
# =============================================================

class LoginPage:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT)
        self.common = Common(driver)

    # ---------------------------------------------------------

    def login(self):

        log.info("Opening Login Page")

        self.driver.get(LOGIN_URL)

        username = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "input[type='email'],input[type='text']"
                )
            )
        )

        username.clear()
        username.send_keys(USERNAME)

        password = self.driver.find_element(
            By.CSS_SELECTOR,
            "input[type='password']"
        )

        password.clear()
        password.send_keys(PASSWORD)

        login_btn = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button[type='submit']"
                )
            )
        )

        self.common.js_click(login_btn)

        self.wait.until(
            lambda d:
            "login" not in d.current_url.lower()
        )

        log.info("Login Successful")


# =============================================================
# AUDIT PAGE
# =============================================================

class AuditSchedulePage:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT)

        self.common = Common(driver)

        self.dropdown = ReactSelect(driver)

    # ---------------------------------------------------------

    def open(self):

        log.info("Opening Audit Schedule")

        self.driver.get(AUDIT_URL)

        self.wait.until(

            EC.presence_of_element_located(

                (
                    By.XPATH,
                    "//button[contains(.,'Advance Search')]"
                )

            )

        )

        log.info("Audit Schedule Loaded")

    # ---------------------------------------------------------

    def click_advance_search(self):

        btn = self.wait.until(

            EC.element_to_be_clickable(

                (
                    By.XPATH,
                    "//button[contains(.,'Advance Search')]"
                )

            )

        )

        self.common.js_click(btn)

        self.common.sleep(1)

    # ---------------------------------------------------------

    def apply_source_filters(self):

        log.info("Applying Source Filters")

        self.dropdown.select(
            "Company",
            SOURCE_COMPANY
        )

        self.wait_company_loaded()

        self.dropdown.select(
            "Associate Company",
            SOURCE_ASSOCIATE
        )

        self.wait_associate_loaded()

        self.dropdown.select(
            "Location",
            SOURCE_LOCATION
        )

        log.info("Company Selected")

        log.info("Associate Company Selected")

        log.info("Location Selected")

    # ---------------------------------------------------------

    def wait_company_loaded(self):

        self.wait.until(

            lambda d:

            self.driver.find_element(

                By.ID,
                "react-select-3-input"

            ).is_enabled()

        )

    # ---------------------------------------------------------

    def wait_associate_loaded(self):

        self.wait.until(

            lambda d:

            self.driver.find_element(

                By.ID,
                "react-select-4-input"

            ).is_enabled()

        )

    # ---------------------------------------------------------

    def click_search(self):

        btn = self.wait.until(

            EC.element_to_be_clickable(

                (
                    By.XPATH,
                    "//button[contains(.,'Advance Search')]"
                )

            )

        )

        self.common.js_click(btn)

        log.info("Search Clicked")

    # ---------------------------------------------------------

    def current_company(self):

        return self.driver.find_element(

            By.XPATH,

            "//small[text()='Company']"
            "/../../div//div[contains(@class,'singleValue')]"

        ).text.strip()

    # ---------------------------------------------------------

    def current_associate(self):

        return self.driver.find_element(

            By.XPATH,

            "//small[text()='Associate Company']"
            "/../../div//div[contains(@class,'singleValue')]"

        ).text.strip()

    # ---------------------------------------------------------

    def current_location(self):

        return self.driver.find_element(

            By.XPATH,

            "//small[text()='Location']"
            "/../../div//div[contains(@class,'singleValue')]"

        ).text.strip()

    # ---------------------------------------------------------

    def verify_filters(self):

        log.info("Verifying Filters")

        assert self.current_company() == SOURCE_COMPANY

        assert self.current_associate() == SOURCE_ASSOCIATE

        assert self.current_location() == SOURCE_LOCATION

        log.info("Filters Verified Successfully")

    # ---------------------------------------------------------

    def clear_company(self):

        inp = self.driver.find_element(
            By.ID,
            "react-select-2-input"
        )

        inp.send_keys(Keys.CONTROL + "a")

        inp.send_keys(Keys.DELETE)

    # ---------------------------------------------------------

    def clear_associate(self):

        inp = self.driver.find_element(
            By.ID,
            "react-select-3-input"
        )

        inp.send_keys(Keys.CONTROL + "a")

        inp.send_keys(Keys.DELETE)

    # ---------------------------------------------------------

    def clear_location(self):

        inp = self.driver.find_element(
            By.ID,
            "react-select-4-input"
        )

        inp.send_keys(Keys.CONTROL + "a")

        inp.send_keys(Keys.DELETE)

    # ---------------------------------------------------------

    def clear_all_filters(self):

        self.clear_location()

        self.clear_associate()

        self.clear_company()

        log.info("Filters Cleared")


# =============================================================
# START DRIVER
# =============================================================

driver = build_driver()

login = LoginPage(driver)

audit = AuditSchedulePage(driver)

login.login()

audit.open()

audit.apply_source_filters()

audit.verify_filters()

audit.click_search()

