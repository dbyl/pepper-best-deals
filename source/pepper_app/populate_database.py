
import datetime
import logging
import logging.config

import pandas as pd
from django.core.management import BaseCommand
from pepper_app.models import PepperArticles, Statistics


class LoadItemDetailesToDatabase(BaseCommand):

    
    def load_to_db(self, item):
        bad = 0
        good = 0
        header = ['item_id', 'name', 'discount_price', 
                'percentage_discount', 'regular_price', 'date_added', 'url']
        item_df = pd.DataFrame(columns=header, data=item)
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
                print(
                    f"goods: {good}, loading time: {start-now}",
                )
            except Exception as e:
                bad += 1
                with open("data_load_logging.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {e} \n")


class LoadDataFromCsv(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "input", type=str, help="Choose directory path with input csv files"
        )

    def handle(self, *args, **options):

        path = options["input"]
        logging.info(f"Preparing data from {path}...")
        df = self.read_csv(path)
        self.load_to_db(df)

    def read_csv(self, directory):
        df = pd.read_csv(directory)
        return df

    def load_to_db(self, df):
        bad = 0
        good = 0
        start = datetime.datetime.now
        for _, row in df.iterrows():
            try:
                region_obj, _ = Region.objects.get_or_create(
                    name=row["region"],
                )
                rank_obj, _ = Rank.objects.get_or_create(
                    name=row["rank"],
                )
                chart_obj, _ = Chart.objects.get_or_create(
                    name=row["chart"],
                )
                artist_obj, _ = Artist.objects.get_or_create(
                    name=row["artist"],
                )
                title_obj, _ = Title.objects.update_or_create(
                    artist=artist_obj,
                    name=row["title"],
                )
                spotifydata_obj, _ = SpotifyData.objects.update_or_create(
                    title=title_obj,
                    rank=rank_obj,
                    date=row["date"],
                    artist=artist_obj,
                    region=region_obj,
                    chart=chart_obj,
                    streams=row["streams"],
                )
                good += 1
                now = datetime.datetime.now
                print(
                    f"goods: {good}, loading time: {start-now}",
                )
            except Exception as e:
                bad += 1
                with open("data_load_logging.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {e} \n")