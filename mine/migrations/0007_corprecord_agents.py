# Generated by Django 2.1 on 2021-10-27 20:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mine', '0006_auto_20211027_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='corprecord',
            name='agents',
            field=models.ManyToManyField(related_name='agent_user', through='mine.CorpAgentRelation', to=settings.AUTH_USER_MODEL),
        ),
    ]
