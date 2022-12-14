# Generated by Django 2.1 on 2022-01-06 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0069_auto_20220105_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldsupcosts',
            name='type',
        ),
        migrations.AddField(
            model_name='fieldsupcosts',
            name='final',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='minereports',
            name='type',
            field=models.CharField(choices=[('Production', 'Production'), ('Engineering', 'Engineering'), ('Env. Mgt.', 'Env. Mgt.'), ('Site Plan', 'Site Plan'), ('Survey', 'Survey'), ('Metallurgical', 'Metallurgical'), ('Geological', 'Geological'), ('Feasibility', 'Feasibility')], max_length=50),
        ),
    ]
