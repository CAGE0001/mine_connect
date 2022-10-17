# Generated by Django 2.1 on 2021-11-30 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0018_auto_20211127_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='mine',
            name='claim',
            field=models.ManyToManyField(through='mine.MineClaimRelation', to='mine.MiningClaim'),
        ),
        migrations.AddField(
            model_name='miningclaim',
            name='mine_attach',
            field=models.CharField(choices=[('None', 'None'), ('Attached', 'Attached')], default='None', max_length=30, null=True),
        ),
    ]