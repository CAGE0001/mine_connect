# Generated by Django 2.1 on 2021-12-07 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0031_auto_20211207_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minemandaterelation',
            name='status',
            field=models.CharField(choices=[('Free', 'Free'), ('Desktop', 'Desktop'), ('Field', 'Field'), ('Exclusive Option', 'Exclusive Option'), ('Negotiation', 'Negotiation'), ('Success', 'Success')], default='Desktop', max_length=30),
        ),
    ]
