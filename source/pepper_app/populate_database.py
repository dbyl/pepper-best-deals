import datetime
import logging
import logging.config
import os
import traceback
import sys
import pandas as pd
from django.core.management import BaseCommand
from pepper_app.models import PepperArticles, ScrapingStatistics


class LoadItemDetailesToDatabase(BaseCommand):

    def __init__(self, item) -> None:
        self.item = item

    def load_to_db(self) -> None:
        header = ['item_id', 'name', 'discount_price',
                'percentage_discount', 'regular_price',
                'date_added', 'url']  #to constans in the future
        data = self.item
        item_df = pd.DataFrame([data], columns=header)
        for _, row in item_df.iterrows():
            try:
                pepperarticles_obj, _ = PepperArticles.objects.get_or_create(
                    item_id = row["item_id"],
                    name = row["name"],
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
        header = ['category_type', 'start_page', 'retrieved_articles_quantity',
                'time_of_the_action', 'action_execution_datetime', 'searched_article',
                'to_csv', 'to_database'] #to constans in the future
        data = self.stats_info
        stats_info_df = pd.DataFrame([data], columns=header)
        for _, row in stats_info_df.iterrows():
            try:
                scrapingstatistics_obj, _ = ScrapingStatistics.objects.get_or_create(
                    category_type = row["category_type"],
                    start_page = row["start_page"],
                    retrieved_articles_quantity = int(row["retrieved_articles_quantity"]),
                    time_of_the_action = row["time_of_the_action"],
                    action_execution_datetime = row["action_execution_datetime"],
                    searched_article = row["searched_article"],
                    to_csv = bool(row["to_csv"]),
                    to_database = bool(row["to_database"]),
                )
            except Exception as e:
                with open("populating_scrapstats_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")

class LoadDataFromCsv(BaseCommand):

    def __init__(self, parser: str) -> None:
        self.parser = parser

    def add_arguments(self) -> None:
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
                pepperarticles_obj, _ = PepperArticles.objects.get_or_create(
                    item_id = row["item_id"],
                    name = row["name"],
                    discount_price = row["discount_price"],
                    percentage_discount = row["percentage_discount"],
                    regular_price = row["regular_price"],
                    date_added = row["date_added"],
                    url = row["url"],
                )
            except Exception as e:
                with open("populating_pepart_from_csv_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {e} \n")