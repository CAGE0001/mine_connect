# Generated by Django 2.1 on 2021-12-09 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0048_auto_20211209_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandateproforma',
            name='amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='mandateproforma',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]