# Generated by Django 3.2.11 on 2022-08-22 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0098_auto_20220822_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miningclaimpolygon',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine.miningclaim'),
        ),
    ]