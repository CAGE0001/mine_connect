# Generated by Django 2.1 on 2021-12-08 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0040_mandaterequest_purpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='mandaterequest',
            name='duration',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]