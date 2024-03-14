import os
import traceback

from django.core.mail import send_mail
from django.db.models import Count, Q
from django.utils import timezone
from pepper_app.environment_config import CustomEnvironment
from pepper_app.models import PepperArticle, User, UserRequest
from pepper_app.populate_database import LoadSuccessfulResponse


class RequestChecking:
    def __init__(self, item):
        self.item_id = item[0]
        self.article_name = item[1]
        self.discount_price = item[2]
        self.url = item[6]

    def check_conditions(
        self,
        request_id,
        desired_article_list,
        article_name_list,
        desired_price,
        discount_price,
        minimum_price,
        user_id,
    ) -> None:
        item_sp = [request_id, timezone.now(), self.item_id]

        matched = all(item in article_name_list for item in desired_article_list)

        try:
            if discount_price == "NA":
                pass
            else:
                if (
                    matched
                    and desired_price >= int(discount_price)
                    and int(discount_price) >= minimum_price
                ):
                    LoadSuccessfulResponse(item_sp).load_to_db()
                    EmailNotifications(user_id, self.item_id).send_alert()
                    UserRequest.objects.filter(request_id=request_id).delete()
        except Exception as e:
            with open("check_conditions_failed.txt", "w") as bad_row:
                bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")

    def matching_request(self) -> None:
        article_name_list = self.article_name.split()
        successful_requests = UserRequest.objects.values_list(
            "request_id", "desired_article", "desired_price", "minimum_price", "user_id"
        )

        try:
            for successful_request in successful_requests:
                request_id = successful_request[0]
                desired_article_list = successful_request[1].split()
                desired_price = successful_request[2]
                minimum_price = successful_request[3]
                user_id = User.objects.values_list("id").get(id=successful_request[4])[
                    0
                ]

                self.check_conditions(
                    request_id,
                    desired_article_list,
                    article_name_list,
                    desired_price,
                    self.discount_price,
                    minimum_price,
                    user_id,
                )
        except Exception as e:
            with open("matching_request_failed.txt", "w") as bad_row:
                bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")


class EmailNotifications:
    def __init__(self, user_id, item_id):
        self.user_id = user_id
        self.item_id = item_id
        self.email = os.environ.get("EMAIL")
        self.article_link = PepperArticle.objects.values_list("url").get(pk=item_id)[0]
        self.user_email = User.objects.values_list("email").get(pk=user_id)

    def send_alert(self):
        subject = "Price alert"
        message = f"The promotion you've been waiting for: {self.article_link}"

        try:
            send_mail(
                subject, message, self.email, self.user_email, fail_silently=False
            )
        except Exception as e:
            with open("sending_emails.txt", "w") as bad_row:
                bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")


class SMSNotifications:
    pass
