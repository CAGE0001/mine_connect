# Generated by Django 2.1 on 2022-01-17 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0079_serviceprov_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claimregcert',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='fieldproviderquote',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='fieldreq',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='minecertificates',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='mineemployees',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='minereports',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='playercertificates',
            name='pdf',
        ),
        migrations.AddField(
            model_name='fieldattachments',
            name='pdf',
            field=models.FileField(blank=True, upload_to='docs/'),
        ),
        migrations.AddField(
            model_name='workhistattach',
            name='pdf',
            field=models.FileField(blank=True, upload_to='docs/'),
        ),
    ]
