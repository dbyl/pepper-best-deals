from pepper_app.models import UserRequest, User, PepperArticle
from django.db.models import Q, Count
from django.utils import timezone
from pepper_app.populate_database import LoadSuccessfulResponse
from smsapi.client import SmsApiPlClient
import traceback
from django.core.mail import send_mail




class RequestChecking:

    def __init__(self, item):
        self.item_id = item[0]
        self.article_name = item[1]
        self.discount_price = item[2]
        self.url = item[6]


    def check_conditions(self, request_id, desired_article_list, article_name_list, desired_price, 
                         discount_price, minimum_price, user_id):

        item_sp = [request_id, timezone.now(), self.item_id]

        matched = all(item in article_name_list for item in desired_article_list)

        try:
            if matched and desired_price >= discount_price and discount_price >= minimum_price:
                LoadSuccessfulResponse(item_sp)
                #send email
                UserRequest.objects.filter(request_id=request_id).delete()
        except Exception as e:
                with open("check_conditions_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")


    def matching_request(self, check_conditions):
        

        article_name_list = self.article_name.split()
        successful_requests = UserRequest.objects.values_list('request_id', 'desired_article', 
                                                               'desired_price', 'minimum_price', 'user_id')

        try:
            for successful_request in successful_requests:
                
                request_id = successful_request[0]
                desired_article_list = successful_request[1].split()
                desired_price = successful_request[2]
                minimum_price = successful_request[3]
                user_id = successful_request[4]
                
                check_conditions(request_id, desired_article_list, article_name_list, 
                                desired_price, self.discount_price, minimum_price, user_id)
        except Exception as e:
                with open("matching_request_failed.txt", "w") as bad_row:
                    bad_row.write(f"Error message: {traceback.format_exc()}, {e} \n")



class EmailNotifications:

    def __init__(self, user_id, article_id):
         
         self.user_id = user_id
         self.article_id = article_id
       
    def send_email(self):
         
         subject = User.objects.get(pk=self.user_id)

         article_link = PepperArticle.objects.values_list('url').get(pk=self.article_id)[0]

         message = f"The promotion you've been waiting for {article_link}"

         
"""
send_mail(
    "Subject here",
    "Here is the message.",
    "from@example.com",
    ["to@example.com"],
    fail_silently=False,
)"""

    


class SMSNotifications:
    pass 




