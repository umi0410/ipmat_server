# Generated by Django 2.2.2 on 2019-08-06 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('food', '0001_initial'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member')),
            ],
        ),
        migrations.CreateModel(
            name='TestRowOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left_food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='left', to='food.Food')),
                ('right_food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='right', to='food.Food')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_test.FoodTest')),
            ],
        ),
    ]
