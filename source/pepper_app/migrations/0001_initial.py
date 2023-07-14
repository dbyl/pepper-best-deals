# Generated by Django 4.2.3 on 2023-07-14 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PepperArticle",
            fields=[
                (
                    "item_id",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=500)),
                (
                    "discount_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                (
                    "percentage_discount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "regular_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                ("date_added", models.DateField()),
                ("url", models.URLField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name="ScrapingStatistic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_type", models.CharField(max_length=500)),
                ("start_page", models.PositiveIntegerField()),
                ("retrieved_articles_quantity", models.PositiveIntegerField()),
                ("time_of_the_action", models.DateTimeField()),
                ("action_execution_datetime", models.DurationField()),
                ("searched_article", models.CharField(max_length=500)),
                ("to_csv", models.BooleanField()),
                ("to_database", models.BooleanField()),
            ],
        ),
    ]
