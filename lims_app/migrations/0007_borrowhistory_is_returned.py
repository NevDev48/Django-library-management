# Generated by Django 5.1.3 on 2024-12-09 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lims_app", "0006_borrowhistory"),
    ]

    operations = [
        migrations.AddField(
            model_name="borrowhistory",
            name="is_returned",
            field=models.BooleanField(default=False),
        ),
    ]
