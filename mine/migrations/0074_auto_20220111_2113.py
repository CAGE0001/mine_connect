# Generated by Django 2.1 on 2022-01-11 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0073_field_mine_owner_requirements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldreq',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Service Choice', 'Service Choice'), ('Proforma', 'Proforma'), ('Expired', 'Expired'), ('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('field', 'field')], max_length=15, null=True),
        ),
    ]
