# Generated by Django 2.1 on 2022-01-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0068_auto_20220104_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serprovprofile',
            name='to_date',
            field=models.DateField(blank=True),
        ),
    ]
