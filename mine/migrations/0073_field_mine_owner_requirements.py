# Generated by Django 2.1 on 2022-01-08 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0072_auto_20220108_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='mine_owner_requirements',
            field=models.ManyToManyField(blank=True, through='mine.FiedlMineRequirements', to='mine.MineJobList'),
        ),
    ]
