# Generated by Django 2.2.2 on 2019-09-12 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0013_food_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]