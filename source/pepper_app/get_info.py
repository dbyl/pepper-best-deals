from datetime import datetime, timedelta, date
import re
from bs4 import BeautifulSoup, Tag
import logging
from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pepper_app.constans import OLD_DATES_DATA_PATTERN_1, OLD_DATES_DATA_PATTERN_2
from enum import Enum, IntEnum
from collections import Counter
import time
from typing import List, Union
import html5lib
import traceback




class Months(Enum):

    sty = '01'
    lut = '02'
    mar = '03'
    kwi = '04'
    maj = '05'
    cze = '06'
    lip = '07'
    sie = '08'
    wrz = '09'
    paz = '10'
    paź = '10'
    lis = '11'
    gru = '12'

    @classmethod
    def to_dict(cls):
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}

    @classmethod
    def keys(cls):
        """Returns a list of all the enum keys."""
        return cls._member_names_

    @classmethod
    def values(cls):
        """Returns a list of all the enum values."""
        return list(cls._value2member_map_.keys())


class GetItemName:

    def __init__(self, article: Tag) -> None:
        self.article = article

    def get_data(self) -> str:
        try:
            name = self.article.find_all(attrs={'class': "cept-tt thread-link linkPlain thread-title--list js-thread-title"})[0]['title']
            return name
        except Exception as e:
            logging.warning(f"Getting item name failed: {e}\n Tracking: {traceback.format_exc()}")


class GetItemId:

    def __init__(self, article: Tag) -> None:
        self.article = article

    def get_data(self) -> int:
        try:
            item_id = self.article.get("id")
            item_id = item_id.strip('thread_')
            item_id = int(item_id)
            return item_id
        except Exception as e:
            logging.warning(f"Getting item id failed: {e}\n Tracking: {traceback.format_exc()}")


class GetItemDiscountPrice:

    def __init__(self, article: Tag) -> None:
        self.article = article

    def get_data(self) -> Union[float, str]:
        try:
            discount_price = self.article.find_all(attrs={'class': "thread-price text--b cept-tp size--all-l size--fromW3-xl"})
            if len(discount_price) > 0:
                discount_price = discount_price[0].get_text().strip('zł').replace('.','').replace(',','.').replace(' ','')
                if discount_price == "ZADARMO":
                    discount_price = float(0)
                else:
                    discount_price = float(discount_price)
            else:
                """The attribute does not exist or the class name is invalid."""
                discount_price = "NA"
            return discount_price
        except Exception as e:
            logging.warning(f"Getting item discount price failed: {e}\n Tracking: {traceback.format_exc()}")



class GetItemRegularPrice:

    def __init__(self, article: Tag) -> None:
        self.article = article

    def get_data(self) -> Union[float, str]:
        try:
            regular_price = self.article.find_all(attrs={'class': "mute--text text--lineThrough size--all-l size--fromW3-xl"})
            if len(regular_price) > 0:
                regular_price = float(regular_price[0].get_text().strip('zł').replace('.','').replace(',','.').replace(' ',''))
            else:
                """The attribute does not exist or the class name is invalid."""
                regular_price = "NA"
            return regular_price
        except Exception as e:
            logging.warning(f"Getting item regular price failed: {e}\n Tracking: {traceback.format_exc()}")



class GetItemPercentageDiscount:

    def __init__(self, article: Tag) -> None:
        self.article = article

    def get_data(self) -> Union[float, str]:
        try:
            percentage_discount = self.article.find_all(attrs={'class': "space--ml-1 size--all-l size--fromW3-xl"})
            if len(percentage_discount) > 0:
                percentage_discount = float(percentage_discount[0].get_text().strip('%'))
            else:
                """The attribute does not exist or the class name is invalid."""
                percentage_discount = "NA"
            return percentage_discount
        except Exception as e:
            logging.warning(f"Getting item percentage discount failed: {e}\n Tracking: {traceback.format_exc()}")


class GetItemUrl:

    def __init__(self, article: Tag) -> None:
        self.article = article

    def get_data(self) -> str:
        try:
            item_url = self.article.find_all('a', {"class":"cept-tt thread-link linkPlain thread-title--list js-thread-title"})[0]['href']
            return item_url
        except Exception as e:
            logging.warning(f"Getting item url failed: {e}\n Tracking: {traceback.format_exc()}")


class GetItemAddedDate:

    def __init__(self, article: Tag) -> None:
        self.article = article

    def get_raw_data(self) -> List[str]:

        try:
            date_tag = self.article.find_all('div', {"class":"size--all-s flex boxAlign-jc--all-fe boxAlign-ai--all-c flex--grow-1 overflow--hidden"})
            raw_string_list = date_tag[0].get_text(strip=True, separator='_').split('_')
            return raw_string_list
        except Exception as e:
            logging.warning(f"Getting item added date failed: {e}\n Tracking: {traceback.format_exc()}")

    def get_data(self) -> str:

        try:
            filtered_list = self.clean_list()
            filtered_list = self.check_missing_date()
            date_string_likely = filtered_list[0]
            if date_string_likely == "NA":
                url_with_item = GetItemUrl.get_data(self)
                soup = self.scrap_page(url_with_item)
                prepared_data = self.fill_missing_date(soup)
                return prepared_data
            else:
                stripped_date_string_likely = self.strip_date_string(date_string_likely)
                prepared_data = self.date_format_conversion(stripped_date_string_likely)
            return prepared_data

        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")

    def strip_date_string(self, date_string_likely: str) -> str:

        try:
            if date_string_likely.startswith("Zaktualizowano ") and date_string_likely.endswith(" temu"):
                stripped_date_string_likely = date_string_likely.lstrip("Zaktualizowano ")
                stripped_date_string_likely = stripped_date_string_likely.rstrip(" temu")
                return stripped_date_string_likely
            elif date_string_likely.endswith("Lokalnie"):
                stripped_date_string_likely = date_string_likely.rstrip("Lokalnie")
                return stripped_date_string_likely
            else:
                stripped_date_string_likely = date_string_likely
                return stripped_date_string_likely
        except Exception as e:
            logging.error(f"Stripping date string failed: {e}\n Tracking: {traceback.format_exc()}")

    def date_format_conversion(self, stripped_date_string_likely: str) -> str:

        try:
            if stripped_date_string_likely.endswith(('min', 'g', 's')):
                prepared_data = date.today().strftime("%Y-%m-%d")
                return prepared_data
            elif stripped_date_string_likely.startswith(tuple(Months.keys())) and len(stripped_date_string_likely) < 8:
                if len(stripped_date_string_likely[4:]) == 3:
                    day = stripped_date_string_likely[4:6]
                else:
                    day = stripped_date_string_likely[4:5].zfill(2)
                month = Months.__members__[stripped_date_string_likely[0:3]].value
                year = str(date.today().year)
                prepared_data = '-'.join([year, month, day])
                return prepared_data
            elif bool(re.search(OLD_DATES_DATA_PATTERN_1, stripped_date_string_likely)):
                day = stripped_date_string_likely[4:6]
                month = Months.__members__[stripped_date_string_likely[0:3]].value
                year = stripped_date_string_likely[8:13]
                prepared_data = '-'.join([year, month, day])
                return prepared_data
            elif bool(re.search(OLD_DATES_DATA_PATTERN_2, stripped_date_string_likely)):
                day = stripped_date_string_likely[4:5].zfill(2)
                month = Months.__members__[stripped_date_string_likely[0:3]].value
                year = stripped_date_string_likely[7:12]
                prepared_data = '-'.join([year, month, day])
                return prepared_data
        except Exception as e:
            logging.error(f"Data format conversion tailed: {e}\n Tracking: {traceback.format_exc()}")


    def clean_list(self) -> List[str]:

        raw_string_list = self.get_raw_data()
        items_to_remove = list()
        filtered_list = list()

        try:
            for string in raw_string_list:
                if "/" in string:
                    items_to_remove.append(string)
                if ":" in string:
                    items_to_remove.append(string)
                if string in ["Jutro", "DZISIAJ", "Lokalnie"]:
                    items_to_remove.append(string)
                if string.startswith("Wysyłka"):
                    items_to_remove.append(string)

            counts = Counter(items_to_remove)

            for string in raw_string_list:
                if counts[string]:
                    counts[string] -= 1
                else:
                    filtered_list.append(string)

            return filtered_list

        except TypeError as e:
            raise TypeError(f"Input data must be a list: {e}")


    def check_missing_date(self) -> List[str]:

        filtered_list = self.clean_list()

        try:
            if len(filtered_list) == 0:
                filtered_list.append("NA")
                return filtered_list
            else:
                return filtered_list
        except TypeError as e:
            raise TypeError(f"Input data must be a list: {e}")


    def fill_missing_date(self, soup) -> str:

        try:
            date_string = soup.find_all('div', {"class":"space--mv-3"})[0].find('span')['title']
            filtered_list = date_string.split()
            day_string = filtered_list[0]
            month_string = filtered_list[1]
            year_string = filtered_list[2].strip(',')

            if len(day_string[0]) == 2:
                day = day_string
            else:
                day = day_string.zfill(2)

            month = Months.__members__[month_string].value
            year = year_string
            prepared_data = '-'.join([year, month, day])
            return prepared_data
        except TypeError as e:
            raise TypeError(f"Input data must be a list: {e}")


    def scrap_page(self, url_with_item: str, driver: WebDriver=None) -> BeautifulSoup:

        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            if driver is None:
                driver = webdriver.Chrome(options=options)
            driver.get(url_with_item)
            time.sleep(0.7)
            page_with_item = driver.page_source
            soup = BeautifulSoup(page_with_item, 'html5lib')
            return soup
        except ConnectionError as e:
            raise ConnectionError(f"ConnectionError occured: {e}. \nTry again later")
        except MissingSchema as e:
            raise MissingSchema(f"MissingSchema occured: {e}. \nMake sure that protocol indicator is icluded in the website url")
        except HTTPError as e:
            raise HTTPError(f"HTTPError occured: {e}. \nMake sure that website url is valid")
        except ReadTimeout as e:
            raise ReadTimeout(f"ReadTimeout occured: {e}. \nTry again later")
