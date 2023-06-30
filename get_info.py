from datetime import datetime, timedelta, date
import re
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
from enum import Enum, IntEnum
from collections import Counter
from selenium import webdriver
import time

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

    def __init__(self, article):
        self.article = article

    def get_data(self):
        try:
            name = self.article.find_all(attrs={'class': "cept-tt thread-link linkPlain thread-title--list js-thread-title"})
            name = name[0].get_text()
            return name
        except IndexError as e:
            raise IndexError(f"Index out of the range: {e}")
        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")


class GetItemId:

    def __init__(self, article):
        self.article = article

    def get_data(self):
        try:
            item_id = self.article["id"]
            item_id = item_id.strip('thread_')
            return item_id
        except IndexError as e:
            raise IndexError(f"Index out of the range: {e}")
        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")


class GetItemDiscountPrice:

    def __init__(self, article):
        self.article = article

    def get_data(self):
        try:
            discount_price = self.article.find_all(attrs={'class': "thread-price text--b cept-tp size--all-l size--fromW3-xl"})
            discount_price = float(discount_price[0].get_text().strip('zł').replace('.','').replace(',','.'))
            return discount_price
        except IndexError as e:
            return "NA"
        except ValueError as e:
            return "NA"
        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")



class GetItemRegularPrice:

    def __init__(self, article):
        self.article = article

    def get_data(self):
        try:
            regular_price = self.article.find_all(attrs={'class': "mute--text text--lineThrough size--all-l size--fromW3-xl"})
            regular_price = float(regular_price[0].get_text().strip('zł').replace('.','').replace(',','.'))
            return regular_price
        except IndexError as e:
            return "NA"
        except ValueError as e:
            return "NA"
        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")


class GetItemPercentageDiscount:

    def __init__(self, article):
        self.article = article

    def get_data(self):
        try:
            percentage_discount = self.article.find_all(attrs={'class': "space--ml-1 size--all-l size--fromW3-xl"})
            percentage_discount = float(percentage_discount[0].get_text().strip('%'))
            return percentage_discount
        except IndexError as e:
            return "NA"
        except ValueError as e:
            return "NA"
        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")


class GetItemUrl:

    def __init__(self, article):
        self.article = article

    def get_data(self):
        try:
            item_url = self.article.find_all('a', href=True, text=True)
            item_url = item_url[0]['href']
            return item_url
        except IndexError as e:
            raise IndexError(f"Index out of the range: {e}")
        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")


class GetItemAddedDate:

    def __init__(self, article):
        self.article = article

    def get_raw_data(self):

        try:
            date_tag = self.article.find_all('div', {"class":"size--all-s flex boxAlign-jc--all-fe boxAlign-ai--all-c flex--grow-1 overflow--hidden"})
            raw_string_list = date_tag[0].get_text(strip=True, separator='_').split('_')
            return raw_string_list
        except IndexError as e:
            raise IndexError(f"Index out of the range: {e}")
        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")

    def get_data(self):

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


    def data_format_conversion(self, date_string_likely):

        old_dates_data_pattern = "[A-Za-z]+\s\d\d\.\s[0-9]+"

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
                prepared_data = date.today().strftime("%d-%m-%Y")
                return prepared_data
            elif date_string_likely.startswith(tuple(Months.keys())) and len(date_string_likely) < 8:
                if len(date_string_likely[4:]) == 3:
                    day = date_string_likely[4:6]
                else:
                    day = date_string_likely[4:5].zfill(2)
                month = Months.__members__[date_string_likely[0:3]].value
                year = str(date.today().year)
                prepared_data = '-'.join([str(day), month, year])
                return prepared_data
            elif bool(re.search(old_dates_data_pattern, date_string_likely)):
                day = date_string_likely[4:6]
                month = Months.__members__[date_string_likely[0:3]].value
                year = date_string_likely[8:13]
                prepared_data = '-'.join([day, month, year])
                return prepared_data
            elif date_string_likely == 'NA': #need to fill NA with date between
                missing_date = date_string_likely
                return missing_date
            elif date_string_likely == 'NA': #need to fill NA with date between
                date_string_to_list = self.check_missing_date_1()
                if len(date_string_to_list[0]) == 2:
                    day = date_string_to_list[0]
                else:
                    day = date_string_to_list[0].zfill(2)
                month = Months.__members__[date_string_to_list[1]].value
                year = date_string_to_list[2][:4]
                prepared_data = '-'.join([str(day), month, year])
                prepared_data = date_string_likely
                return prepared_data

        except KeyError as e:
            raise KeyError(f"Invalid name of the month {e}")


    def get_strings_list_to_filter(self):

        try:
            date_class = self.article.find_all('div', {"class":"size--all-s flex boxAlign-jc--all-fe boxAlign-ai--all-c flex--grow-1 overflow--hidden"})
            raw_string_list = date_class[0].get_text(strip=True, separator='_').split('_')

            return raw_string_list
        except TypeError as e:
            raise TypeError(f"Invalid html class name: {e}")


    def clean_list(self):

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


    def check_missing_date(self):

        filtered_list = self.clean_list()

        try:
            if len(filtered_list) == 0:
                filtered_list.append("NA")
                return filtered_list
            else:
                return filtered_list
        except TypeError as e:
            raise TypeError(f"Input data must be a list: {e}")


    def fill_missing_date(self):

        try:
            url_with_item = GetItemUrl.get_data(self)
            driver = webdriver.Chrome('./chromedriver')
            driver.get(url_with_item)
            time.sleep(0.7)
            page_with_item = driver.page_source
            soup = BeautifulSoup(page_with_item, 'html.parser')
            return soup
        except ConnectionError as e:
            print(f"ConnectionError occured: {e}. \nTry again later")
        except MissingSchema as e:
            print(f"MissingSchema occured: {e}. \nMake sure that protocol indicator is icluded in the website url")
        except HTTPError as e:
            print(f"HTTPError occured: {e}. \nMake sure that website url is valid")
        except ReadTimeout as e:
            print(f"ReadTimeout occured: {e}. \nTry again later")

            date_string = soup.find_all('div', {"class":"space--mv-3"})[0].find('span')['title']
            time.sleep(0.1)
            filtered_list = date_string.split()
            day_string = filtered_list[0]
            month_string = filtered_list[1]
            year_string = filtered_list[2]

            if len(day_string[0]) == 2:
                day = day_string
            else:
                day = day_string.zfill(2)

            month = Months.__members__[month_string].value
            year = year_string
            prepared_data = '-'.join([day, month, year])
            return prepared_data
        except TypeError as e:
            raise TypeError(f"Input data must be a list: {e}")





