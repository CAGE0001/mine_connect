# Generated by Django 3.2.11 on 2022-12-28 02:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mine', '0125_auto_20221228_0409'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorksDev',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('dev_date', models.DateField()),
                ('comment', models.CharField(blank=True, max_length=2000, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('works', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.mineworks')),
            ],
        ),
    ]
