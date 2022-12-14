# Generated by Django 3.2.11 on 2022-06-15 04:32

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mine', '0093_auto_20220615_0114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mine',
            name='location',
        ),
        migrations.RemoveField(
            model_name='mine',
            name='polygon',
        ),
        migrations.RemoveField(
            model_name='miningclaim',
            name='beacons',
        ),
        migrations.RemoveField(
            model_name='miningclaim',
            name='location',
        ),
        migrations.RemoveField(
            model_name='miningclaim',
            name='polygon',
        ),
        migrations.CreateModel(
            name='MiningClaimPolygon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('location', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.miningclaim')),
            ],
        ),
        migrations.CreateModel(
            name='MiningClaimLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.miningclaim')),
            ],
        ),
        migrations.CreateModel(
            name='MiningClaimBeacons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('location', django.contrib.gis.db.models.fields.MultiPointField(blank=True, null=True, srid=4326)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.miningclaim')),
            ],
        ),
        migrations.CreateModel(
            name='MinePolygon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.mine')),
            ],
        ),
        migrations.CreateModel(
            name='MineLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.mine')),
            ],
        ),
    ]
