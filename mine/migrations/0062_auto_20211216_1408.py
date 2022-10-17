# Generated by Django 2.1 on 2021-12-16 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0061_fieldreq_provider_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldreq',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Service Choice', 'Service Choice'), ('Proforma', 'Proforma'), ('Expired', 'Expired'), ('Cancelled', 'Cancelled'), ('Approved', 'Approved')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='serviceprovrequired',
            name='field_request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine.FieldReq'),
        ),
    ]
