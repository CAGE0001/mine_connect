# Generated by Django 2.1 on 2021-12-08 05:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mine', '0035_miningclaim_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='MineInvestReq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('invest_type', models.CharField(choices=[('Purchase', 'Purchase'), ('JV', 'Joint-Venture'), ('Tribute', 'Tribute'), ('Manage', 'Raising Contract')], max_length=100)),
                ('value', models.FloatField()),
                ('valid', models.DateField()),
                ('status', models.CharField(choices=[('Free', 'Free'), ('Cart', 'Cart'), ('Field', 'Field'), ('Mandate', 'Mandate'), ('Un-Available', 'Un-Available')], default='Free', max_length=20, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='mine',
            name='status',
        ),
        migrations.AddField(
            model_name='mineinvestreq',
            name='mine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mine'),
        ),
    ]