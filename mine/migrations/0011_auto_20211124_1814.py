# Generated by Django 2.1 on 2021-11-24 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0010_auto_20211124_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='trxns',
            name='invoice_ref',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trxns',
            name='reverse_trxn',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='trxns',
            name='payee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trxns_payee', to='mine.Player'),
        ),
        migrations.AlterField(
            model_name='trxns',
            name='payer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine.Player'),
        ),
        migrations.AlterField(
            model_name='trxns',
            name='purpose',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine.TrxnPurpose'),
        ),
    ]
