# Generated by Django 5.1.3 on 2024-11-30 06:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lims_app", "0002_category_book"),
    ]

    operations = [
        migrations.CreateModel(
            name="Book_lib",
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
                ("title", models.CharField(max_length=200)),
                ("author", models.CharField(max_length=100)),
                ("publication_date", models.DateField()),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="book_images/"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books",
                        to="lims_app.category",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Book",
        ),
    ]
