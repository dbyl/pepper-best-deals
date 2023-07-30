from datetime import datetime, timedelta, date
import re
from bs4 import BeautifulSoup, Tag
import logging
from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
from enum import Enum, IntEnum
from collections import Counter
from selenium import webdriver
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
            item_id = self.article.find_all(attrs={'class': "thread cept-thread-item thread--type-list imgFrame-container--scale thread--deal"})[0]['id']
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
                discount_price = float(discount_price[0].get_text().strip('zł').replace('.','').replace(',','.'))
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
                regular_price = float(regular_price[0].get_text().strip('zł').replace('.','').replace(',','.'))
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
                prepared_data = self.fill_missing_date()
                return prepared_data
            else:
                prepared_data = self.data_format_conversion(date_string_likely)
            return prepared_data

        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")


    def data_format_conversion(self, date_string_likely: str) -> str:

        old_dates_data_pattern = r"[A-Za-z]+\s\d\d\.\s[0-9]+"

        try:
            if date_string_likely.startswith("Zaktualizowano ") and date_string_likely.endswith(" temu"):
                date_string_likely = date_string_likely.lstrip("Zaktualizowano ")
                date_string_likely = date_string_likely.rstrip(" temu")
            elif date_string_likely.endswith("Lokalnie"):
                date_string_likely = date_string_likely.rstrip("Lokalnie")
        except Exception:
            return date_string_likely

        try:
            if date_string_likely.endswith(('min', 'g', 's')):
                prepared_data = date.today().strftime("%Y-%m-%d")
                return prepared_data
            elif date_string_likely.startswith(tuple(Months.keys())) and len(date_string_likely) < 8:
                if len(date_string_likely[4:]) == 3:
                    day = date_string_likely[4:6]
                else:
                    day = date_string_likely[4:5].zfill(2)
                month = Months.__members__[date_string_likely[0:3]].value
                year = str(date.today().year)
                prepared_data = '-'.join([year, month, day])
                return prepared_data
            elif bool(re.search(old_dates_data_pattern, date_string_likely)):
                day = date_string_likely[4:6]
                month = Months.__members__[date_string_likely[0:3]].value
                year = date_string_likely[8:13]
                prepared_data = '-'.join([year, month, day])
                return prepared_data


        except KeyError as e:
            raise KeyError(f"Invalid name of the month {e}")


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


    def fill_missing_date(self) -> str:

        try:
            url_with_item = GetItemUrl.get_data(self)
            driver = webdriver.Chrome()
            driver.get(url_with_item)
            time.sleep(0.7)
            page_with_item = driver.page_source
            soup = BeautifulSoup(page_with_item, 'html5lib')
        except ConnectionError as e:
            logging.warning(f"ConnectionError occured: {e}. \nTry again later")
        except MissingSchema as e:
            logging.warning(f"MissingSchema occured: {e}. \nMake sure that protocol indicator is icluded in the website url")
        except HTTPError as e:
            logging.warning(f"HTTPError occured: {e}. \nMake sure that website url is valid")
        except ReadTimeout as e:
            logging.warning(f"ReadTimeout occured: {e}. \nTry again later")

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


