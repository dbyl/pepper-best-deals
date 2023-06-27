from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
import logging
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta, date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from enum import Enum, IntEnum
from collections import Counter 



class ScrapWebpage:

    def __init__(self, website_url, action_type, articles_to_retrieve, start_page=1):
        self.website_url = website_url
        self.action_type = action_type
        self.articles_to_retrieve = articles_to_retrieve
        self.start_page = start_page

    def scrap_data(self):
        try:
            url_to_scrap = self.website_url + self.action_type + str(self.start_page)
            driver = webdriver.Chrome('./chromedriver') 
            driver.set_window_size(1400,1000)
            driver.get(url_to_scrap) 
            time.sleep(0.7)
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            return soup
        except ConnectionError as e:
            print(f"ConnectionError occured: {e}. \nTry again later")
        except MissingSchema as e:
            print(f"MissingSchema occured: {e}. \nMake sure that protocol indicator is icluded in the website url")
        except HTTPError as e:
            print(f"HTTPError occured: {e}. \nMake sure that website url is valid")
        except ReadTimeout as e:
            print(f"ReadTimeout occured: {e}. \nTry again later")

    def infinite_scroll_handling(self):
        try:
            flag = True
            retrived_articles = list()
            while flag:
                soup = self.scrap_data()
                articles = soup.find_all('article')
                retrived_articles += articles
                if len(retrived_articles) >= self.articles_to_retrieve:
                    flag = False
                    return retrived_articles[:self.articles_to_retrieve]
                self.start_page += 1
        except IndexError as e:
            raise IndexError("There aren't that many articles, try retrieve lower quantity of articles")

        
    
    def get_items_details(self):

        retrived_articles = self.infinite_scroll_handling()

        all_items = list()
        for article in retrived_articles:
            item = list()
            item.append(GetItemId(article).get_data())
            item.append(GetItemName(article).get_data())
            item.append(GetItemDiscountPrice(article).get_data())
            item.append(GetItemPercentageDiscount(article).get_data())
            item.append(GetItemRegularPrice(article).get_data())
            #item.append(GetItemAddedDate(article).get_data())
            item.append(GetItemUrl(article).get_data())
            all_items.append(item)

        return all_items

    def dump_articles_to_txt(self):

        retrived_articles = self.infinite_scroll_handling()

        with open("scraped_data.txt", "w") as file:
            for item in retrived_articles:
                file.write(item)

    def read_articles_from_txt(self):

        articles = list()

        with open("scraped_data.txt", "r") as file:
            for item in file:
                article = item[:-1]
                articles.append(article)
        
        return articles


class GetItemName:

    def __init__(self, article):
        self.article = article
    
    def get_data(self):
        try:
            name = self.article.find_all(attrs={'class': "cept-tt thread-link linkPlain thread-title--list js-thread-title"})
            name = name[0].get_text()
            return name
        except IndexError as e:
            raise IndexError(f"Index out of the range (item_name): {e}")
        except TypeError as e:
            raise TypeError(f"Invalid html class name (item_name): {e}")


class GetItemId:

    def __init__(self, article):
        self.article = article

    def get_data(self):
        try:
            item_id = self.article["id"]
            item_id = item_id.strip('thread_')
            return item_id
        except IndexError as e:
            raise IndexError(f"Index out of the range (item_id): {e}")
        except TypeError as e:
            raise TypeError(f"Invalid html class name (item_id): {e}")


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
            raise TypeError(f"Invalid html class name (item_discount_price): {e}")



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
            raise TypeError(f"Invalid html class name (item_regular_price): {e}")


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
            raise TypeError(f"Invalid html class name (item_percentage_discount): {e}")


class GetItemUrl:

    def __init__(self, article):
        self.article = article
    
    def get_data(self):
        try:
            item_url = self.article.find_all('a', href=True, text=True)
            item_url = item_url[0]['href']
            return item_url
        except IndexError as e:
            raise IndexError(f"Index out of the range (item_url): {e}")
        except TypeError as e:
            raise TypeError(f"Invalid html class name (item_url): {e}")

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


class GetItemAddedDate:

    def __init__(self, article):
        self.article = article

    def get_data(self):
        try:
            date_tag = self.article.find_all(attrs={'class': "metaRibbon lbox--v-1 boxAlign-ai--all-c overflow--wrap-off space--l-3 text--color-greyShade"})
            #date = self.find_true_date(date_tag)
            return date_tag
        except IndexError as e:
            raise IndexError(f"Index out of the range (item_url): {e}")
        except TypeError as e:
            raise TypeError(f"Invalid html class name (item_url): {e}")

    def find_true_date(self, date_tag):


        try:
            true_data = self.first_index_date_searching(date_tag)
            print("1")
            return true_data
        except Exception:
            print("bad1")
            try:
                true_data = self.second_index_date_searching(date_tag)
                print("2")
                return true_data
            except Exception:
                print("bad2")
                try:
                    true_data = self.third_index_date_searching(date_tag)
                    print("3")
                    return true_data
                except Exception:
                    print("bad3")


    def data_format_conversion(self, date_string_likely):

        old_dates_data_pattern = "[A-Za-z]+\s\d\d\.\s[0-9]+"

        try:
            if date_string_likely.startswith("Zaktualizowano"):
                date_string_likely = date_string_likely.lstrip("Zaktualizowano ") 
            elif date_string_likely.endswith("Lokalnie"):
                date_string_likely = date_string_likely.rstrip("Lokalnie") 
        except Exception:
            return date_string_likely

        try:
            if date_string_likely.endswith(('min', 'g', 's', 'temu')):
                prepared_data = date.today().strftime("%d-%m-%Y")
                return prepared_data
            elif date_string_likely.startswith(tuple(Months.keys())) and len(date_tag) < 8:      
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
        except KeyError as e:
            raise KeyError(f"Invalid name of the month {e}")


    def first_index_date_searching(self, date_tag):

        output_data_pattern = "\d{2}[/.-]\d{2}[/.-]\d{4}"

        
        #date = self.data_format_conversion(date_string_likely)

        try:
            date_string_likely = date_tag[0].get_text()
            formatted_data = self.data_format_conversion(date_string_likely)
            if bool(re.search(output_data_pattern, formatted_data)):
                return formatted_data
            else:
                raise Exception
        except Exception as e:
            print(e)

    def second_index_date_searching(self, date_tag):
        
        output_data_pattern = "\d{2}[/.-]\d{2}[/.-]\d{4}"

        
        #date = self.data_format_conversion(date_string_likely)

        try:
            date_string_likely = date_tag[1].get_text()
            formatted_data = self.data_format_conversion(date_string_likely)
            if bool(re.search(output_data_pattern, formatted_data)):
                return formatted_data
            else:
                raise Exception
        except Exception as e:
            print(e)

    def third_index_date_searching(self, date_tag):
        
        output_data_pattern = "\d{2}[/.-]\d{2}[/.-]\d{4}"

        
        #date = self.data_format_conversion(date_string_likely)

        try:
            date_string_likely = date_tag[2].get_text()
            formatted_data = self.data_format_conversion(date_string_likely)
            if bool(re.search(output_data_pattern, formatted_data)):
                return formatted_data
            else:
                raise Exception
        except Exception as e:
            print(e)



action_type = "/nowe?page="
start_page = 1
website_url = "https://www.pepper.pl"
articles_to_retrieve = 800

data = ScrapWebpage(website_url, action_type, articles_to_retrieve, start_page)

articles = data.infinite_scroll_handling()
#data.dump_articles_to_txt()
#articles = data.read_articles_from_txt()


n = 1 
from collections import Counter 

def get_strings_list_to_filter(article):

    try:
        date_class = article.find_all('div', {"class":"size--all-s flex boxAlign-jc--all-fe boxAlign-ai--all-c flex--grow-1 overflow--hidden"})
        all_strings_list = date_class[0].get_text(strip=True, separator='_').split('_')

        return all_strings_list
    except TypeError as e:
        raise TypeError(f"Invalid html class name (item_url): {e}")

def clean_list(all_strings_list):

    items_to_remove = list()
    counts = Counter(items_to_remove)
    filtered_list = list()

    try:
        for string in all_strings_list:
            if "/" in string:
                items_to_remove.append(string)
            if ":" in string:
                items_to_remove.append(string)
            if string in ["Jutro", "DZISIAJ", "Lokalnie"]:
                items_to_remove.append(string)
            if string.startswith("Wysyłka"):
                items_to_remove.append(string)
        
        counts = Counter(items_to_remove)

        for string in all_strings_list:
            if counts[string]:
                counts[string] -= 1
            else:
                filtered_list.append(string)
        
        return filtered_list

    except TypeError as e:
        raise TypeError(f"Input data must be a list: {e}")


def check_missing_date(filtered_list):
    
    try:
        if len(filtered_list) == 0:
            filtered_list.append("NA")
            return filtered_list
        else:
            return filtered_list
    except TypeError as e:
        raise TypeError(f"Input data must be a list: {e}")

def get_from_date_tag(date_tag):

    try:
        date_class = date_tag[0].get_text()
        all_strings_list = date_class[0].get_text(strip=True, separator='_').split('_')

        return all_strings_list
    except TypeError as e:
        raise TypeError(f"Invalid html class name (item_url): {e}")


def save_data(name, filtered_list, n):

    with open("info.txt", "a") as file:
        file.write(str(name) + '\n')
        file.write(str(filtered_list) + '\n')
        file.write(str(n) + '\n')




previous_date = list()
for article in articles:

    
    
    out = GetItemAddedDate(article)
    date_tag = out.get_data()

    print(article)

    name = article.find_all('a', {"class":"cept-tt thread-link linkPlain thread-title--list js-thread-title"})[0].get_text()
    #all_strings_list = get_from_date_tag(date_tag)
    all_strings_list = get_strings_list_to_filter(article)
    filtered_list = clean_list(all_strings_list)
    filtered_list = check_missing_date(filtered_list)

    save_data(name, filtered_list, n)
    

    #print(name.title())
    #print(filtered_list)
    #print(date_tag)
    #print(f"len: {len(spans)}")
    #print(f"number: {n}")
    n += 1

