# Generated by Django 5.1.3 on 2024-12-04 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lims_app", "0004_jurnal"),
    ]

    operations = [
        migrations.AddField(
            model_name="reader",
            name="password",
            field=models.CharField(default="", max_length=200),
        ),
    ]