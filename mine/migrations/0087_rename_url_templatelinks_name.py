# Generated by Django 3.2.11 on 2022-02-02 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0086_auto_20220202_1223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='templatelinks',
            old_name='url',
            new_name='name',
        ),
    ]
