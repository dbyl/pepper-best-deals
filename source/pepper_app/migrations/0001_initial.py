# Generated by Django 4.2.7 on 2024-01-02 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PepperArticle",
            fields=[
                (
                    "item_id",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                ("article_name", models.CharField(max_length=500)),
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
                ("stats_id", models.AutoField(primary_key=True, serialize=False)),
                ("category_type", models.CharField(max_length=500)),
                ("retrieved_articles_quantity", models.PositiveIntegerField()),
                ("time_of_the_action", models.DateTimeField()),
                ("action_execution_datetime", models.DurationField()),
                (
                    "searched_article",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("to_csv", models.BooleanField()),
                ("to_database", models.BooleanField()),
                ("scrap_continuously", models.BooleanField()),
                ("scrap_choosen_data", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="UserRequest",
            fields=[
                ("request_id", models.AutoField(primary_key=True, serialize=False)),
                ("request_time", models.DateTimeField()),
                (
                    "desired_article",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "desired_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=20, null=True
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SuccessfulResponse",
            fields=[
                ("response_id", models.AutoField(primary_key=True, serialize=False)),
                ("response_time", models.DateTimeField()),
                (
                    "item_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pepper_app.pepperarticle",
                    ),
                ),
                (
                    "request_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pepper_app.userrequest",
                    ),
                ),
            ],
        ),
    ]
