# Generated by Django 2.1 on 2022-01-14 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0078_field_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprov',
            name='summary',
            field=models.TextField(blank=True, max_length=3000),
        ),
    ]
