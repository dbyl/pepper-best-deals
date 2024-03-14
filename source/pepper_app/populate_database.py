import logging
import logging.config
import traceback

import pandas as pd
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.utils import timezone
from pepper_app.constans import (
    DATA_HEADER,
    REQUEST_HEADER,
    RESPONSE_HEADER,
    STATS_HEADER,
)
from pepper_app.models import (
    PepperArticle,
    ScrapingStatistic,
    SuccessfulResponse,
    UserRequest,
)


class LoadUserRequestToDatabase(BaseCommand):
    def __init__(self, item: list) -> None:
        self.item = item

    def load_to_db(self) -> None:
        data = self.item
        item_df = pd.DataFrame([data], columns=REQUEST_HEADER)
        for _, row in item_df.iterrows():
            try:
                userrequest_obj, _ = UserRequest.objects.get_or_create(
                    desired_article=row["desired_article"].lower(),
                    desired_price=row["desired_price"],
                    minimum_price=row["minimum_price"],
                    user_id=row["user_id"],
                    request_time=row["request_time"],
                )
            except Exception as e:
                with open("populating_requests_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")


class LoadSuccessfulResponse(BaseCommand):
    def __init__(self, item_sp: list) -> None:
        self.item_sp = item_sp

    def load_to_db(self) -> None:
        data = self.item_sp
        response_df = pd.DataFrame([data], columns=RESPONSE_HEADER)
        for _, row in response_df.iterrows():
            try:
                successfulresponse_obj, _ = SuccessfulResponse.objects.get_or_create(
                    request_id=row["request_id"],
                    response_time=row["response_time"],
                    item_id=PepperArticle.objects.get(item_id=row["item_id"]),
                )
            except Exception as e:
                with open("populating_responses_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")


class LoadItemDetailsToDatabase(BaseCommand):
    def __init__(self, item: list) -> None:
        self.item = item

    def load_to_db(self) -> None:
        data = self.item
        item_df = pd.DataFrame([data], columns=DATA_HEADER)
        for _, row in item_df.iterrows():
            try:
                pepperarticle_obj, _ = PepperArticle.objects.get_or_create(
                    item_id=row["item_id"],
                    article_name=row["name"],
                    discount_price=self.na_discount_price(row),
                    percentage_discount=self.na_percentage_discount(row),
                    regular_price=self.na_regular_price(row),
                    date_added=row["date_added"],
                    url=row["url"],
                )
            except Exception as e:
                with open("populating_detailstodb_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")

    def na_discount_price(self, row: pd.Series):
        if row["discount_price"] == "NA":
            return None
        else:
            return float(row["discount_price"])

    def na_percentage_discount(self, row: pd.Series):
        if row["percentage_discount"] == "NA":
            return None
        else:
            return float(row["percentage_discount"])

    def na_regular_price(self, row: pd.Series):
        if row["regular_price"] == "NA":
            return None
        else:
            return float(row["regular_price"])


class LoadScrapingStatisticsToDatabase(BaseCommand):
    def __init__(self, stats_info: list) -> None:
        self.stats_info = stats_info

    def load_to_db(self) -> None:
        data = self.stats_info
        stats_info_df = pd.DataFrame([data], columns=STATS_HEADER)
        for _, row in stats_info_df.iterrows():
            try:
                scrapingstatistic_obj, _ = ScrapingStatistic.objects.get_or_create(
                    category_type=row["category_type"],
                    retrieved_articles_quantity=int(row["retrieved_articles_quantity"]),
                    time_of_the_action=row["time_of_the_action"],
                    action_execution_datetime=row["action_execution_datetime"],
                    searched_article=self.if_no_search_item(row),
                    to_csv=bool(row["to_csv"]),
                    to_database=bool(row["to_database"]),
                    scrape_continuously=bool(row["scrape_continuously"]),
                    scrape_choosen_data=bool(row["scrape_choosen_data"]),
                )
            except Exception as e:
                with open("populating_scrapestats_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")

    def if_no_search_item(self, row: pd.Series):
        if row["category_type"] == "nowe":
            return None
        else:
            return row["searched_article"]
