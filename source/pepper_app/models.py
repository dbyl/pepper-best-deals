from django.db import models
from django.contrib.auth.models import User



class PepperArticle(models.Model):

    item_id = models.PositiveIntegerField(primary_key=True)
    article_name = models.CharField(max_length=500)
    discount_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    percentage_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    regular_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    date_added = models.DateField()
    url = models.URLField(max_length = 300)

    def __str__(self):

        fields = [str(self.item_id), str(self.article_name), str(self.discount_price), str(self.percentage_discount),
                str(self.regular_price), str(self.date_added), str(self.url)]

        return ', '.join(fields)

class ScrapingStatistic(models.Model):

    stats_id = models.AutoField(primary_key=True)
    category_type = models.CharField(max_length=500)
    start_page = models.PositiveIntegerField()
    retrieved_articles_quantity = models.PositiveIntegerField()
    time_of_the_action = models.DateTimeField()
    action_execution_datetime = models.DurationField()
    searched_article = models.CharField(max_length=500,  null=True, blank=True)
    to_csv = models.BooleanField()
    to_database = models.BooleanField()
    scrap_continuously = models.BooleanField()
    scrap_choosen_data = models.BooleanField()


    def __str__(self):
        fields = [str(self.stats_id), str(self.category_type), str(self.start_page), str(self.retrieved_articles_quantity),
                str(self.time_of_the_action), str(self.action_execution_datetime), str(self.searched_article),
                str(self.to_csv), str(self.to_database), str(self.scrap_continuously), str(self.scrap_choosen_data)]

        return ', '.join(fields)

class UserRequest(models.Model):

    request_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    request_time = models.DateTimeField()
    desired_article = models.CharField(max_length=500,  null=True, blank=True)
    desired_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        fields = [str(self.request_id), str(self.user), str(self.request_time), str(self.desired_article), str(self.desired_price)]

class SuccessfulResponse(models.Model):

    response_id = models.AutoField(primary_key=True)
    request_id = models.ForeignKey(UserRequest, on_delete=models.CASCADE)
    response_time = models.DateTimeField()
    item_id = models.ForeignKey(PepperArticle, on_delete=models.CASCADE)


    def __str__(self):
        fields = [str(self.response_id), str(self.request_id), str(self.response_time)]



