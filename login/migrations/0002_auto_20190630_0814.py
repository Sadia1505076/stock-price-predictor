# Generated by Django 2.2.1 on 2019-06-30 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
