# Generated by Django 2.2.1 on 2019-08-27 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_sharehistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharehistory',
            name='trade_code',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shareprediction',
            name='trade_code',
            field=models.CharField(max_length=50),
        ),
    ]
