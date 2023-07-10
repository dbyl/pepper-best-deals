
import datetime
import logging
import logging.config
import os

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'source.configuration.settings.py')

#django.setup()


import pandas as pd
from django.db import models
from django.core.management import BaseCommand
#from pepper_app.models import PepperArticles, Statistics





class LoadItemDetailesToDatabase(BaseCommand):

    def __init__(self, item) -> None:
        self.article = article

    def load_to_db(self) -> None:
        bad = 0
        good = 0
        header = ['item_id', 'name', 'discount_price',
                'percentage_discount', 'regular_price',
                'date_added', 'url']
        item_df = pd.DataFrame(columns=header, data=self.item)
        start = datetime.datetime.now
        for _, row in item_df.iterrows():
            try:
                pepperarticles_obj, _ = PepperArticles.objects.update_or_create(
                    item_id = row["item_id"],
                    name = row["name"],
                    discount_price = row["discount_price"],
                    percentage_discount = row["percentage_discount"],
                    regular_price = row["regular_price"],
                    date_added = row["date_added"],
                    url = row["url"],
                )
                good += 1
                now = datetime.datetime.now
                logger.info(f"goods: {good}, loading time: {start-now}")
            except Exception as e:
                bad += 1
                with open("populating_db_errors.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {e} \n")


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
        bad = 0
        good = 0
        start = datetime.datetime.now
        for _, row in df.iterrows():
            try:
                pepperarticles_obj, _ = PepperArticles.objects.update_or_create(
                    item_id = row["item_id"],
                    name = row["name"],
                    discount_price = row["discount_price"],
                    percentage_discount = row["percentage_discount"],
                    regular_price = row["regular_price"],
                    date_added = row["date_added"],
                    url = row["url"],
                )
                good += 1
                now = datetime.datetime.now
                logger.info(f"goods: {good}, loading time: {start-now}")
            except Exception as e:
                bad += 1
                with open("data_load_logging.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {e} \n")