# Generated by Django 2.2.2 on 2019-09-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_auto_20190905_0700'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodbook',
            name='playCount',
            field=models.IntegerField(default=0),
        ),
    ]
