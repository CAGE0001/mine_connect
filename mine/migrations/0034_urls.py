# Generated by Django 2.1 on 2021-12-07 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0033_auto_20211207_0401'),
    ]

    operations = [
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
            ],
        ),
    ]
