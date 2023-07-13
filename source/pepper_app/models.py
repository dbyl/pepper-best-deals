from django.db import models


class PepperArticle(models.Model):

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

class ScrapingStatistic(models.Model):

    category_type = models.CharField(max_length=500)
    start_page = models.PositiveIntegerField()
    retrieved_articles_quantity = models.PositiveIntegerField()
    time_of_the_action = models.DateTimeField()
    action_execution_datetime = models.DurationField()
    searched_article = models.CharField(max_length=500)
    to_csv = models.BooleanField()
    to_database = models.BooleanField()


    def __str__(self):
        fields = [str(self.category_type), str(self.start_page), str(self.retrieved_articles_quantity),
                str(self.time_of_the_action), str(self.action_execution_datetime), str(self.searched_article),
                str(self.to_csv), str(self.to_database)]

        return ', '.join(fields)

