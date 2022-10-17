# Generated by Django 2.1 on 2022-01-19 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0081_auto_20220118_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldattachments',
            name='pdf',
            field=models.FileField(blank=True, upload_to='docs/'),
        ),
        migrations.AlterField(
            model_name='fieldreq',
            name='pdf',
            field=models.FileField(null=True, upload_to='docs/'),
        ),
        migrations.AlterField(
            model_name='mineemployees',
            name='pdf',
            field=models.FileField(blank=True, upload_to='docs/'),
        ),
        migrations.AlterField(
            model_name='minereports',
            name='pdf',
            field=models.FileField(null=True, upload_to='docs/'),
        ),
        migrations.AlterField(
            model_name='playercertificates',
            name='pdf',
            field=models.FileField(null=True, upload_to='images/certificates/'),
        ),
        migrations.AlterField(
            model_name='workhistattach',
            name='pdf',
            field=models.FileField(blank=True, upload_to='docs/'),
        ),
    ]
