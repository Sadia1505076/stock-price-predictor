# Generated by Django 2.2.1 on 2019-08-28 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_sharehistory_shareprediction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShareHistory',
        ),
        migrations.DeleteModel(
            name='SharePrediction',
        ),
    ]