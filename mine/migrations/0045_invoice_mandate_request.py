# Generated by Django 2.1 on 2021-12-09 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0044_auto_20211209_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='mandate_request',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mine.MandateRequest'),
            preserve_default=False,
        ),
    ]
