# Generated by Django 2.1 on 2021-12-13 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0056_auto_20211213_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='playercertificates',
            name='pdf',
            field=models.ImageField(null=True, upload_to='images/reports/'),
        ),
    ]
