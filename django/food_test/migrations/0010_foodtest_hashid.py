# Generated by Django 2.2.2 on 2019-08-09 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_test', '0009_testrows_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodtest',
            name='hashId',
            field=models.CharField(default=1111, max_length=5),
            preserve_default=False,
        ),
    ]