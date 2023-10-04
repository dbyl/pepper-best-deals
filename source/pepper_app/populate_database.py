import datetime
import logging
import logging.config
from pepper_app.constans import DATA_HEADER, STATS_HEADER
from datetime import timezone
import os
import traceback
import sys
import pandas as pd
from django.core.management import BaseCommand
from pepper_app.models import PepperArticle, ScrapingStatistic


class LoadItemDetailsToDatabase(BaseCommand):

    def __init__(self, item) -> None:
        self.item = item

    def load_to_db(self) -> None:
        data = self.item
        item_df = pd.DataFrame([data], columns=DATA_HEADER)
        for _, row in item_df.iterrows():
            try:
                pepperarticle_obj, _ = PepperArticle.objects.get_or_create(
                    item_id = row["item_id"],
                    article_name = row["name"],
                    discount_price = self.na_discount_price(row),
                    percentage_discount = self.na_percentage_discount(row),
                    regular_price = self.na_regular_price(row),
                    date_added = row["date_added"],
                    url = row["url"],
                )
            except Exception as e:
                with open("populating_pepart_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")

    def na_discount_price(self, row):

        if row["discount_price"] == 'NA':
            return None
        else:
            return float(row["discount_price"])

    def na_percentage_discount(self, row):
        if row["percentage_discount"] == 'NA':
            return None
        else:
            return float(row["percentage_discount"])

    def na_regular_price(self, row):
        if row["regular_price"] == 'NA':
            return None
        else:
            return float(row["regular_price"])

class LoadScrapingStatisticsToDatabase(BaseCommand):

    def __init__(self, stats_info) -> None:
        self.stats_info = stats_info

    def load_to_db(self) -> None:
        data = self.stats_info
        stats_info_df = pd.DataFrame([data], columns=STATS_HEADER)
        for _, row in stats_info_df.iterrows():
            try:
                scrapingstatistic_obj, _ = ScrapingStatistic.objects.get_or_create(
                    category_type = row["category_type"],
                    start_page = row["start_page"],
                    retrieved_articles_quantity = int(row["retrieved_articles_quantity"]),
                    time_of_the_action = row["time_of_the_action"],
                    action_execution_datetime = row["action_execution_datetime"],
                    searched_article = self.if_no_search_item(row),
                    to_csv = bool(row["to_csv"]),
                    to_database = bool(row["to_database"]),
                    scrap_continuously = bool(row["scrap_continuously"]),
                    scrap_choosen_data = bool(row["scrap_choosen_data"])
                )
            except Exception as e:
                with open("populating_scrapstats_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")

    def if_no_search_item(self, row):
        if row["category_type"] == 'nowe':
            return None
        else:
            return row["searched_article"]

class LoadDataFromCsv(BaseCommand):

    """
    def __init__(self, parser: str) -> None:
        self.parser = parser
    """

    def add_arguments(self, parser: str) -> None:
        self.parser.add_argument(
            "input", type=str, help="Choose directory path with input csv files"
        )

    def handle(self, *args, **options) -> None:
        path = options["input"]
        logging.info(f"Preparing data from {path}...")
        df = self.read_csv(path)
        self.load_to_db(df)

    def read_csv(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df

    def load_to_db(self, df) -> None:
        for _, row in df.iterrows():
            try:
                pepperarticle_obj, _ = PepperArticle.objects.get_or_create(
                    item_id = row["item_id"],
                    article_name = row["name"],
                    discount_price = row["discount_price"],
                    percentage_discount = row["percentage_discount"],
                    regular_price = row["regular_price"],
                    date_added = row["date_added"],
                    url = row["url"],
                )
            except Exception as e:
                with open("populating_pepart_from_csv_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {e} \n")