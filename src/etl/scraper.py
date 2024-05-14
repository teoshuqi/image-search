import time
from datetime import datetime
from typing import List, Optional

import pytz
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (
    JavascriptException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By

from src.config import WEBDRIVER_HOST, WEBDRIVER_PORT

from .product import Product


class WebsiteScraper:
    """
    A class to scrape data from the website from fashion ecommerce websites.
    get_all_product_info() method is the main method used to extract all
    available product information into a specified product class into a list.
    """

    def __init__(
        self,
        base_url: str,
        url_product_prefix: str,
        product_tag: str,
        product_tag_attribute: dict,
        next_page_xpath: str,
        next_page_script: str,
        product_class: type,
        button_xpath: str,
        button_script: str,
    ):
        self.base_url = base_url
        self.url_product_prefix = url_product_prefix
        self.product_tag = product_tag
        self.product_tag_attribute = product_tag_attribute
        self.next_page_xpath = next_page_xpath
        self.next_page_script = next_page_script
        self.product_class = product_class
        self.button_xpath = button_xpath
        self.button_script = button_script
        self._driver = None
        self._product_listing = None

    def get_all_product_info(self, max_pages: Optional[int] = 100) -> List[Product]:
        """
        Extracts all product information from the website
        and returns a list of dictionaries.

        Returns:
            A list of dictionaries, each containing
            extracted product information.
        """

        self._get_driver()
        self._go_to_website()
        self._click_button()
        self._scroll_to_bottom()
        prev_url = "previous_url"
        pg = 1
        all_products = []

        while self._has_next_page(prev_url):
            prev_url = self._driver.current_url
            page_source = self._driver.page_source
            page_products = self._get_products_from_page(page_source)
            if (len(page_products) > 0) & (pg <= max_pages):
                all_products.extend(page_products)

                self._click_next_page()
                pg += 1
                self._click_button()
                self._scroll_to_bottom()
                print(self._driver.current_url, len(page_products))
            else:
                break

        self._quit_driver()
        return all_products

    def _has_next_page(self, prev_url: str) -> bool:
        current_url = self._driver.current_url
        if (prev_url != current_url) & (self.next_page_xpath != ""):
            return True
        else:
            return False

    def _get_products_from_page(self, page_source: str) -> List[Product]:
        """
        Extracts product information from a single page source.

        Args:
            page_source: The HTML source of the page.

        Returns:
            A list of dictionaries containing product information.
        """
        now_datetime = datetime.now(pytz.timezone("Asia/Singapore"))
        soup = BeautifulSoup(page_source, "html.parser")
        product_listing = soup.find_all(self.product_tag, self.product_tag_attribute)

        if len(product_listing) > 0:
            products = []
            for product in product_listing:
                prd = self.product_class(product, now_datetime, self.base_url)
                products.append(prd)
            return products
        else:
            return []

    def _get_driver(self):
        """
        Provides a headless Chrome driver for scraping.

        Returns:
        """
        print("                ###### _get_driver")
        url = f"http://{WEBDRIVER_HOST}:{WEBDRIVER_PORT}"
        # options = webdriver.ChromeOptions()
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--disable-extensions')
        # options.add_argument('--remote-debugging-port=9222')
        # options.add_argument('--log-level=DEBUG')
        # options.add_argument('--enable-logging')
        # options.add_argument('--disable-software-rasterizer')
        # options.add_argument("--disable-notifications")
        # options.add_argument("--disable-infobars")
        options = webdriver.FirefoxOptions()
        options.headless = False
        self._driver = webdriver.Remote(url, options=options)
        self._driver.get("http://google.com")
        print("     testing:", self._driver.title, self._driver.current_url)
        return

    def _go_to_website(self):
        current_url = self.base_url + self.url_product_prefix
        self._driver.get(current_url)

    def _quit_driver(self):
        """
        Quits a headless Chrome driver for scraping.

        Returns:
        """
        self._driver.quit()
        return

    def _click_button(self):
        try:
            if len(self.button_xpath) > 0:
                button_element = self._driver.find_element(By.XPATH, self.button_xpath)
                self._driver.execute_script(self.button_script, button_element)
                time.sleep(1)
        except (NoSuchElementException, JavascriptException) as e:
            print(f"cannot find button due to {type(e).__name__} from xpath: {self.button_xpath}.")
            return False
        return True

    def _click_next_page(self):
        """
        Clicks the next page element if present.

        Args:
            current_url: The current URL of the page.

        Returns:
        """
        try:
            self._close_window_handles()
            next_page_element = self._driver.find_element(By.XPATH, self.next_page_xpath)
            self._driver.execute_script(self.next_page_script, next_page_element)
            time.sleep(0.5)
        except (NoSuchElementException, JavascriptException) as e:
            print(f"cannot find next page button due to {type(e).__name__} from xpath: {self.next_page_xpath}.")

    def _scroll_to_bottom(self):
        """
        Scrolls to the bottom of webpage
        """
        try:
            height_script = "return document.body.scrollHeight"
            height = self._driver.execute_script(height_script)
            if height is None:
                height = 26888
            total_height = int(height)
            for i in range(1, total_height, 30):
                scroll_script = f"window.scrollTo(0, {i});"
                self._driver.execute_script(scroll_script)
            time.sleep(0.5)

        except (NoSuchElementException, JavascriptException) as e:
            print(f"cannot scroll to bottom of page due to {type(e).__name__}.")

    def _close_window_handles(self):
        parent = self._driver.current_window_handle
        uselessWindows = self._driver.window_handles
        for winId in uselessWindows:
            if winId != parent:
                self._driver.switch_to.window(winId)
                self._driver.close()
