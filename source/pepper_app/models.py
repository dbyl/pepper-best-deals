from django.db import models
from django.db.models import Model


class PepperArticles(Model):

    item_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=500)
    discount_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    percentage_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    regular_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    date_added = models.DateField()
    url = models.URLField(max_length = 300)

    def __str__(self):

        fields = [str(self.item_id), str(self.name), str(self.discount_price), str(self.percentage_discount),
                str(self.regular_price), str(self.date_added), str(self.url)]

        return ', '.join(fields)

class Statistics(Model):

    action_type = models.CharField(max_length=500)
    retrieved_articles_quantity = models.PositiveIntegerField()
    searched_article = models.CharField(max_length=500)
    time_of_the_action = models.DateTimeField()
    action_execution_datetime = models.TimeField()

    def __str__(self):
        fields = [str(self.action_type), str(self.retrieved_articles_quantity), str(self.searched_article),
                str(self.time_of_the_action), str(self.action_execution_datetime)]

