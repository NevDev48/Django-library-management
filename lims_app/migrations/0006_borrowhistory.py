# Generated by Django 5.1.3 on 2024-12-09 05:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lims_app", "0005_reader_password"),
    ]

    operations = [
        migrations.CreateModel(
            name="BorrowHistory",
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
                ("borrowed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="borrow_history",
                        to="lims_app.book_lib",
                    ),
                ),
                (
                    "reader",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="borrowed_books",
                        to="lims_app.reader",
                    ),
                ),
            ],
        ),
    ]
