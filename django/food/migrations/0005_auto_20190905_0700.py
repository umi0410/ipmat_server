# Generated by Django 2.2.2 on 2019-09-05 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_food_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='oneline_desc',
            field=models.CharField(max_length=30),
        ),
    ]