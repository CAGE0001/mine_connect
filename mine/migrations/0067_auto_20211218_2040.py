# Generated by Django 2.1 on 2021-12-18 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0066_auto_20211218_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldproviderquote',
            name='counter_offer',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fieldproviderquote',
            name='comment',
            field=models.CharField(blank=True, max_length=1055),
        ),
        migrations.AlterField(
            model_name='fieldproviderquote',
            name='pdf',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='fieldproviderquote',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Submitted', 'Submitted'), ('Counter Offer', 'Counter Offer'), ('Success', 'Success')], default='Pending', max_length=15),
        ),
    ]