# Generated by Django 2.1 on 2021-12-17 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0065_auto_20211217_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serprovprofile',
            name='engagement',
        ),
        migrations.AlterField(
            model_name='serprovprofile',
            name='principal',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='serprovprofile',
            name='reference',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
