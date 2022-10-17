# Generated by Django 2.1 on 2021-10-18 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartMineRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CorpRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('Pvt Ltd', 'Private (Limited)'), ('Ltd', 'Public'), ('PBC', 'PBC')], max_length=20)),
                ('doi', models.DateField(verbose_name='Date of Inc')),
                ('reg_number', models.CharField(max_length=50, verbose_name='Identity Number')),
                ('agents', models.ManyToManyField(related_name='agent_user', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('nationality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Country')),
            ],
        ),
        migrations.CreateModel(
            name='MineCertificates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('type', models.CharField(choices=[('Mine Manager', 'Mine Manager'), ('EMA', 'EMA'), ('Inspection', 'Inspection'), ('Explosives Storage', 'Explosives Storage'), ('Explosives Transport', 'Explosives Transport'), ('Non Encumberance', 'Non Encumberance')], max_length=50)),
                ('issue_date', models.DateField(null=True)),
                ('pdf', models.CharField(max_length=255, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MineClaimRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Current', 'Current'), ('Tributed', 'Tributed'), ('Sold', 'Sold'), ('Forfeited', 'Forfeited')], default='Current', max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MineMandateRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Desktop', 'Desktop'), ('Field', 'Field'), ('Exclusive Option', 'Exclusive Option'), ('Negotiation', 'Negotiation'), ('Success', 'Success')], default='Current', max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MineMandateRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(default='Pending', max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MineMineral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MineOwnerRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Current', 'Current'), ('Tributed', 'Tributed'), ('Sold', 'Sold'), ('Forfeited', 'Forfeited')], default='Current', max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MineReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('type', models.CharField(choices=[('Production', 'Production'), ('Engineering', 'Engineering'), ('Env. Mgt.', 'Env. Mgt.'), ('Site Plan', 'Site Plan'), ('Survey', 'Survey'), ('Metallurgical', 'Metallurgical'), ('Geological', 'Geological')], max_length=50)),
                ('report_date', models.DateField(null=True)),
                ('pdf', models.CharField(max_length=255, null=True)),
                ('digital', models.CharField(max_length=255, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerCertificates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('type', models.CharField(choices=[('Incorporation', 'Incorporation'), ('Directors', 'Directors'), ('Syndicate Agreement', 'Syndicate Agreement'), ('Personal ID', 'Personal ID')], max_length=30)),
                ('issue_date', models.DateField(null=True)),
                ('pdf', models.CharField(max_length=255, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='corporate',
            name='agents',
        ),
        migrations.RemoveField(
            model_name='corporate',
            name='author',
        ),
        migrations.RemoveField(
            model_name='corporate',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='dircert',
            name='author',
        ),
        migrations.RemoveField(
            model_name='dircert',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='engreport',
            name='author',
        ),
        migrations.RemoveField(
            model_name='engreport',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='envmgtreport',
            name='author',
        ),
        migrations.RemoveField(
            model_name='envmgtreport',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='explstocert',
            name='author',
        ),
        migrations.RemoveField(
            model_name='explstocert',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='expltrnscert',
            name='author',
        ),
        migrations.RemoveField(
            model_name='expltrnscert',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='georeport',
            name='author',
        ),
        migrations.RemoveField(
            model_name='georeport',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='incorpcert',
            name='author',
        ),
        migrations.RemoveField(
            model_name='incorpcert',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='author',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='inspeccert',
            name='author',
        ),
        migrations.RemoveField(
            model_name='inspeccert',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='metreport',
            name='author',
        ),
        migrations.RemoveField(
            model_name='metreport',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='minemgrcert',
            name='author',
        ),
        migrations.RemoveField(
            model_name='minemgrcert',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='nonencumbcert',
            name='author',
        ),
        migrations.RemoveField(
            model_name='nonencumbcert',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='persid',
            name='author',
        ),
        migrations.RemoveField(
            model_name='persid',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='prodreport',
            name='author',
        ),
        migrations.RemoveField(
            model_name='prodreport',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='surveyreport',
            name='author',
        ),
        migrations.RemoveField(
            model_name='surveyreport',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='syndagree',
            name='author',
        ),
        migrations.RemoveField(
            model_name='syndagree',
            name='syndicate',
        ),
        migrations.RemoveField(
            model_name='cartminematch',
            name='mines',
        ),
        migrations.RemoveField(
            model_name='mandate',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='mandaterequest',
            name='mines',
        ),
        migrations.RemoveField(
            model_name='mine',
            name='mineral',
        ),
        migrations.RemoveField(
            model_name='mine',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='miningclaim',
            name='mine',
        ),
        migrations.RemoveField(
            model_name='syndicate',
            name='owner',
        ),
        migrations.AddField(
            model_name='beacon',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='beacon',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='beacon',
            name='symbol',
            field=models.CharField(default='A', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='miningclaim',
            name='status',
            field=models.CharField(choices=[('Current', 'Current'), ('Tributed', 'Tributed'), ('Sold', 'Sold'), ('Forfeited', 'Forfeited')], default='Current', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='ref',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='syndicate',
            name='name',
            field=models.CharField(default='Synd', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='beacon',
            name='geometry',
            field=models.CharField(choices=[('PMB', 'Precious Metal'), ('BMB', 'Base Metal'), ('SGE', 'Special Grant Exploration'), ('SGM', 'Special Grant Mining'), ('SB', 'Special Block'), ('ESGE', 'Energy Special Grant Exploration'), ('ESGM', 'Energy Special Grant Mining')], max_length=50),
        ),
        migrations.AlterField(
            model_name='beacon',
            name='mining_claim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.MiningClaim'),
        ),
        migrations.AlterField(
            model_name='fieldinvoice',
            name='field_proforma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_proforma', to='mine.FieldProforma'),
        ),
        migrations.AlterField(
            model_name='fieldproforma',
            name='field_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.FieldReq'),
        ),
        migrations.AlterField(
            model_name='fieldreq',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Proforma', 'Proforma'), ('Expired', 'Expired'), ('Cancelled', 'Cancelled'), ('Approved', 'Approved')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='mine',
            name='status',
            field=models.CharField(choices=[('Free', 'Free'), ('Cart', 'Cart'), ('Field', 'Field'), ('Mandate', 'Mandate')], default='Free', max_length=20),
        ),
        migrations.AlterField(
            model_name='mineemployees',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mine.IndRecord'),
        ),
        migrations.AlterField(
            model_name='miningclaim',
            name='type',
            field=models.CharField(choices=[('PMB', 'Precious Metal'), ('BMB', 'Base Metal'), ('SGE', 'Special Grant Exploration'), ('SGM', 'Special Grant Mining'), ('SB', 'Special Block'), ('ESGE', 'Energy Special Grant Exploration'), ('ESGM', 'Energy Special Grant Mining')], max_length=50),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='type',
            field=models.CharField(choices=[('Individual', 'Individual'), ('Corporate', 'Corporate'), ('Syndicate', 'Syndicate')], max_length=30),
        ),
        migrations.AlterField(
            model_name='serprovprofile',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.IndRecord'),
        ),
        migrations.DeleteModel(
            name='Corporate',
        ),
        migrations.DeleteModel(
            name='DirCert',
        ),
        migrations.DeleteModel(
            name='EngReport',
        ),
        migrations.DeleteModel(
            name='EnvMgtReport',
        ),
        migrations.DeleteModel(
            name='ExplStoCert',
        ),
        migrations.DeleteModel(
            name='ExplTrnsCert',
        ),
        migrations.DeleteModel(
            name='GeoReport',
        ),
        migrations.DeleteModel(
            name='IncorpCert',
        ),
        migrations.DeleteModel(
            name='Individual',
        ),
        migrations.DeleteModel(
            name='InspecCert',
        ),
        migrations.DeleteModel(
            name='MetReport',
        ),
        migrations.DeleteModel(
            name='MineMgrCert',
        ),
        migrations.DeleteModel(
            name='NonEncumbCert',
        ),
        migrations.DeleteModel(
            name='PersId',
        ),
        migrations.DeleteModel(
            name='ProdReport',
        ),
        migrations.DeleteModel(
            name='SurveyReport',
        ),
        migrations.DeleteModel(
            name='SyndAgree',
        ),
        migrations.AddField(
            model_name='playercertificates',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Player'),
        ),
        migrations.AddField(
            model_name='minereports',
            name='mine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mine'),
        ),
        migrations.AddField(
            model_name='mineownerrelation',
            name='mine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mine'),
        ),
        migrations.AddField(
            model_name='mineownerrelation',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Player'),
        ),
        migrations.AddField(
            model_name='minemineral',
            name='mine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mine'),
        ),
        migrations.AddField(
            model_name='minemineral',
            name='mineral',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mineral'),
        ),
        migrations.AddField(
            model_name='minemandaterequest',
            name='mandate_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.MandateRequest'),
        ),
        migrations.AddField(
            model_name='minemandaterequest',
            name='mine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mine'),
        ),
        migrations.AddField(
            model_name='minemandaterelation',
            name='mandate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mandate'),
        ),
        migrations.AddField(
            model_name='minemandaterelation',
            name='mine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mine'),
        ),
        migrations.AddField(
            model_name='mineclaimrelation',
            name='claim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.MiningClaim'),
        ),
        migrations.AddField(
            model_name='mineclaimrelation',
            name='mine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mine'),
        ),
        migrations.AddField(
            model_name='minecertificates',
            name='mine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mine'),
        ),
        migrations.AddField(
            model_name='cartminerelation',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.CartMineMatch'),
        ),
        migrations.AddField(
            model_name='cartminerelation',
            name='mine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mine.Mine'),
        ),
        migrations.AddField(
            model_name='mine',
            name='claims',
            field=models.ManyToManyField(through='mine.MineClaimRelation', to='mine.MiningClaim'),
        ),
    ]