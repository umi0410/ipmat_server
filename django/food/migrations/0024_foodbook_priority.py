# Generated by Django 2.2.2 on 2019-09-12 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0023_remove_food_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodbook',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
