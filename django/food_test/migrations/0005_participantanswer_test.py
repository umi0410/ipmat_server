# Generated by Django 2.2.2 on 2019-09-02 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_test', '0004_remove_participantanswer_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='participantanswer',
            name='test',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food_test.FoodTest'),
            preserve_default=False,
        ),
    ]