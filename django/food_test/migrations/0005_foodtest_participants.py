# Generated by Django 2.2.2 on 2019-08-09 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
        ('food_test', '0004_participantanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodtest',
            name='participants',
            field=models.ManyToManyField(related_name='part', to='member.Member'),
        ),
    ]
