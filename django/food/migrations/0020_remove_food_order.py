# Generated by Django 2.2.2 on 2019-09-12 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0019_food_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='order',
        ),
    ]
