from django.db import models
from django.db.models import Model

class Name(Model):

    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class DiscountPrice(Model):

    discount_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return self.discount_price

class PercentageDiscount(Model):

    percentage_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return self.percentage_discount

class RegularPrice(Model):

    regular_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return self.regular_price

class Url(Model):

    url = models.URLField(max_length = 300)

    def __str__(self):
        return self.url

class ActionType(Model):

    action_type = models.CharField(max_length=500)

    def __str__(self):
        return self.action_type

class RetrievedArticlesQuantity(Model):

    retrieved_articles_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.retrieved_articles_quantity

class SearchedArticle(Model):

    searched_article = models.CharField(max_length=300)

    def __str__(self):
        return self.searched_article

########################################################################################

class PepperArticles(Model):

    item_id = models.PositiveIntegerField(primary_key=True, on_delete=models.CASCADE)
    name = models.ForeignKey(Name, on_delete=models.CASCADE)
    discount_price = models.ForeignKey(DiscountPrice, on_delete=models.CASCADE)
    percentage_discount = models.ForeignKey(PercentageDiscount, on_delete=models.CASCADE)
    regular_price = models.ForeignKey(RegularPrice, on_delete=models.CASCADE)
    date_added = models.DateField(on_delete=models.CASCADE)
    url = ForeignKey(Url, on_delete=models.CASCADE)

    def __str__(self):

        fields = [self.item_id, self.name, self.discount_price, self.percentage_discount,
                self.regular_price, self.date_added, self.url]

        return ', '.join(fields)

class Statistics(Model):

    action_type = models.ForeignKey(ActionType, on_delete=models.CASCADE)
    retrieved_articles_quantity = models.ForeignKey(RetrievedArticlesQuantity, on_delete=models.CASCADE)
    searched_article = models.ForeignKey(SearchedArticle, on_delete=models.CASCADE)
    time_of_the_action = models.DateTimeField()
    action_execution_datetime = models.TimeField()

