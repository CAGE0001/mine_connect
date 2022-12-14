# Generated by Django 2.1 on 2022-01-04 03:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mine', '0067_auto_20211218_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkHistAttach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('type', models.CharField(choices=[('Contract', 'Contract'), ('Letter', 'Letter'), ('Invoice', 'Invoice'), ('Plan', 'Plan'), ('Report', 'Report')], max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.ServiceProv')),
            ],
        ),
        migrations.AddField(
            model_name='fieldsupcosts',
            name='type',
            field=models.CharField(choices=[('Budget', 'Budget'), ('Final', 'Final')], default='Budget', max_length=8),
        ),
    ]
