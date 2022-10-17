# Generated by Django 2.1 on 2021-11-30 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0019_auto_20211130_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WorksList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('works', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='YellowList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='mineplant',
            old_name='compressor_comment',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='mineworks',
            old_name='cyanide_tanks_comment',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='mineyellowplant',
            old_name='compressor_comment',
            new_name='comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='compressor',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='conveyor',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='conveyor_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='crusher',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='crusher_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='gravity_separator',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='gravity_separator_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='head_gear',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='head_gear_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='hoist',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='hoist_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='jackhammer',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='jackhammer_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='mill',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='mill_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='ore_bin',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='ore_bin_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='pick',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='pick_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='rail',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='rail_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='shovel',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='shovel_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='wheel_barrow',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='wheel_barrow_comment',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='windlass',
        ),
        migrations.RemoveField(
            model_name='mineplant',
            name='windlass_comment',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='cyanide_tanks',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='dump',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='dump_comment',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='level',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='level_comment',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='shaft',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='shaft_comment',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='stope',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='stope_comment',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='tunnel',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='tunnel_comment',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='ventilation',
        ),
        migrations.RemoveField(
            model_name='mineworks',
            name='ventilation_comment',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='compressor',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='dozer',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='dozer_comment',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='drill_rig',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='drill_rig_comment',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='dumper',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='dumper_comment',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='fel',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='fel_comment',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='grader',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='grader_comment',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='horse',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='horse_comment',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='low_bed',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='low_bed_comment',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='trailer',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='trailer_comment',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='vehicle',
        ),
        migrations.RemoveField(
            model_name='mineyellowplant',
            name='vehicle_comment',
        ),
        migrations.AddField(
            model_name='mineplant',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mineworks',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mineyellowplant',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mineplant',
            name='plant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine.PlantList'),
        ),
        migrations.AddField(
            model_name='mineworks',
            name='works',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine.WorksList'),
        ),
        migrations.AddField(
            model_name='mineyellowplant',
            name='plant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine.YellowList'),
        ),
    ]