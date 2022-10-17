# Generated by Django 2.1 on 2021-12-06 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0028_investorminerelation_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='MandateTypeList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='mandaterequest',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mine.MandateTypeList'),
        ),
    ]
