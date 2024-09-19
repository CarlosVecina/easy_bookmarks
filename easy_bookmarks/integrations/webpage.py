import datetime
import logging

import bs4
import numpy as np
import polars as pl
from bs4 import BeautifulSoup
from pydantic import model_validator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from easy_bookmarks.integrations.base_integration import (
    BaseBookmark,
    BaseIntegration,
    BaseListBookmarks,
)

logger = logging.getLogger(__name__)


class WebpageBookmark(BaseBookmark):
    url: str
    title: str
    description: str
    reference_date: datetime.datetime
    extra_data: str | None = None
    uuid: str | None = None

    uuid_fields: list[str] = ["url", "title"]


class ListWebpageBookmarks(BaseListBookmarks):
    root: list[WebpageBookmark]

    def to_polars_dataframe(self) -> pl.DataFrame:
        return pl.DataFrame([bookmark.model_dump() for bookmark in self.root])


class BaseWebpageIntegration(BaseIntegration):
    base_urls: list[str]
    driver: webdriver.Chrome | None = None

    source: str = "webpage"
    soup: bs4.BeautifulSoup | None = None

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, **data):
        super().__init__(**data)
        if self.driver is None:
            self.driver = self.get_driver()

    @staticmethod
    def get_driver(use_proxy=False):
        chrome_options = Options()
        chrome_options = webdriver.ChromeOptions()

        if use_proxy:
            driver = webdriver.Chrome(
                ChromeDriverManager().install(), chrome_options=chrome_options
            )
            driver.get("https://sslproxies.org/")
            driver.execute_script(
                "return arguments[0].scrollIntoView(true);",
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]",
                        )
                    )
                ),
            )
            ips = [
                my_elem.get_attribute("innerHTML")
                for my_elem in WebDriverWait(driver, 5).until(
                    EC.visibility_of_all_elements_located(
                        (
                            By.XPATH,
                            "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]",
                        )
                    )
                )
            ]
            ports = [
                my_elem.get_attribute("innerHTML")
                for my_elem in WebDriverWait(driver, 5).until(
                    EC.visibility_of_all_elements_located(
                        (
                            By.XPATH,
                            "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]",
                        )
                    )
                )
            ]
            proxies = []
            for i in range(0, len(ips)):
                proxies.append(ips[i] + ":" + ports[i])
            chrome_options = webdriver.ChromeOptions()
            i = int(np.random.randint(low=0, high=5, size=(1,)))
            chrome_options.add_argument("--proxy-server={}".format(proxies[i]))
            chrome_options.add_argument("start-maximized")
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_experimental_option("useAutomationExtension", False)

        chrome_options.add_argument("start-maximized")
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
            },
        )

        return driver

    def load_page(self, url: str):
        self.driver.get(url)
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, "html.parser")
        ...


class PwCWebpageIntegration(BaseWebpageIntegration):
    # trending research
    base_urls: list[str] = ["https://paperswithcode.com/"]
    n_pages: int | None = 5

    @model_validator(mode="after")
    def validate_coherence(self):
        if (
            self.base_urls != ["https://paperswithcode.com/"]
            and self.base_urls != ["https://paperswithcode.com/latest/"]
        ) and self.n_pages is not None:
            raise ValueError(
                "`n_pages` must be None if `base_urls` is not the default value"
            )
        return self

    def __init__(self, **data):
        super().__init__(**data)
        if self.base_urls == ["https://paperswithcode.com/"]:
            # page 0 partial results
            self.base_urls = [
                f"https://paperswithcode.com/?page={i}"
                for i in range(1, self.n_pages + 1)
            ]
        else:
            self.base_urls = [
                f"https://paperswithcode.com/latest/?page={i}"
                for i in range(1, self.n_pages + 1)
            ]

    def _compose_bookmark(self, element: bs4.ResultSet):
        return WebpageBookmark(
            url=element.find_all("a")[0].get("href"),
            title=element.find_all("a")[1].text,
            description=element.find_all("p", class_="item-strip-abstract")[0].text,
            reference_date=datetime.datetime.strptime(
                element.find_all("span", class_="author-name-text item-date-pub")[
                    0
                ].text,
                "%d %b %Y",
            ),
            extra_data=", ".join(
                f"{k}: {v}"
                for k, v in {
                    "stars": element.find_all("div", class_="entity-stars")[
                        0
                    ].text.strip()
                }.items()
            ),
        )

    def get_bookmarks(self) -> ListWebpageBookmarks:
        bookmarks = []
        for base_url in self.base_urls:
            self.load_page(base_url)
            for element in self.soup.find_all(
                "div", class_="row infinite-item item paper-card"
            ):
                bookmarks.append(self._compose_bookmark(element))
        return ListWebpageBookmarks(bookmarks)

    def get_bookmarks_df(self) -> pl.DataFrame:
        bookmarks = self.get_bookmarks()
        return pl.from_records(bookmarks.model_dump())
