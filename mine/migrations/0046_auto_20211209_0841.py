# Generated by Django 2.1 on 2021-12-09 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0045_invoice_mandate_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trxns',
            name='amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='trxns',
            name='invoice_ref',
            field=models.IntegerField(default=0, null=True),
        ),
    ]