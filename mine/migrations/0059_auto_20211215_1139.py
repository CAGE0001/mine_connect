# Generated by Django 2.1 on 2021-12-15 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0058_auto_20211214_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceprovrequired',
            name='field_request',
        ),
        migrations.RemoveField(
            model_name='serviceprovrequired',
            name='provider_role',
        ),
        migrations.DeleteModel(
            name='ServiceProvRequired',
        ),
    ]
