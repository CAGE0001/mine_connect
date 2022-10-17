from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations
from django.utils.datetime_safe import datetime


class Migration(migrations.Migration):

    operations = [
        CreateExtension('postgis'),
    ]


SEX = (
    ('M', 'Male'),
    ('F', 'Female'),
)

PLAYERS = (
    ('Individual', 'Individual'),
    ('Corporate', 'Corporate'),
    ('Syndicate', 'Syndicate'),
)

CORPTYPE = (
    ('Pvt Ltd', '(Private) Limited'),
    ('Ltd', 'Public'),
    ('PBC', 'PBC'),
)

MINECLAIM = (
    ('PMB', 'Precious Metal'),
    ('BMB', 'Base Metal'),
    ('SGE', 'Special Grant Exploration'),
    ('SGM', 'Special Grant Mining'),
    ('SB', 'Special Block'),
    ('ESGE', 'Energy Special Grant Exploration'),
    ('ESGM', 'Energy Special Grant Mining'),
)

TRANSACTOR = (
    ('Investor', 'Investor'),
    ('Mine Owner', 'Mine Owner'),
    ('Prof Service', 'Prof Service'),
    ('MC Suspense Account', 'Mining Connect'),
    ('External Source', 'External Source'),
    ('Corporate', 'Corporate'),
    ('Advertiser', 'Advertiser'),
    ('Ext', 'External')
)

GOLDRESOURCE = (
    ('BIF', 'Banded Ironstone'),
    ('Quartz', 'Quartz'),
    ('SG', 'Special Grant'),
    ('SB', 'Special Block')
)

CHROMERESOURCE = (
    ('Pod', 'Podiform'),
    ('Alluvial', 'Alluvial'),
    ('Dump', 'Dump'),
    ('Seam', 'Seam')
)

INVESTYPE = (
    ('Purchase', 'Purchase'),
    ('JV', 'Joint-Venture'),
    ('Tribute', 'Tribute'),
    ('Manage', 'Raising Contract')
)

OWNERSTATUS = (
    ('Current', 'Current'),
    ('Tributed', 'Tributed'),
    ('Sold', 'Sold'),
    ('Forfeited', 'Forfeited')
)

MINECERTIFICATES = (
    ('Mine Manager', 'Mine Manager'),
    ('EMA', 'EMA'),
    ('Inspection', 'Inspection'),
    ('Explosives Storage', 'Explosives Storage'),
    ('Explosives Transport', 'Explosives Transport'),
    ('Non Encumberance', 'Non Encumberance'),
)

MINEREPORTS = (
    ('Production', 'Production'),
    ('Engineering', 'Engineering'),
    ('Env. Mgt.', 'Env. Mgt.'),
    ('Site Plan', 'Site Plan'),
    ('Survey', 'Survey'),
    ('Metallurgical', 'Metallurgical'),
    ('Geological', 'Geological'),
    ('Feasibility', 'Feasibility'),
)

MINEAGREEMENTS = (
    ('Tribute', 'Tribute'),
    ('Joint Venture', 'Joint Venture'),
    ('Management.', 'Management'),
)

MINERECEIPTS = (
    ('Inspection', 'Inspection'),
    ('Registration', 'Registration'),
    ('Site', 'Site'),
    ('Explosives', 'Explosives'),
    ('Fine', 'Fine'),
    ('Other', 'Other'),
)

MINELETTERS = (
    ('Mines Ministry', 'Mines Ministry'),
    ('Government', 'Government'),
    ('Other', 'Other'),
)

PLAYERCERT = (
    ('Incorporation', 'Incorporation'),
    ('Directors', 'Directors'),
    ('Syndicate Agreement', 'Syndicate Agreement'),
    ('Personal ID', 'Personal ID'),
)

MANDATESTATUS = (
    ('Free', 'Free'),
    ('Desktop', 'Desktop'),
    ('Field', 'Field'),
    ('Exclusive Option', 'Exclusive Option'),
    ('Negotiation', 'Negotiation'),
    ('Success', 'Success'),
)

MEMBERSTATUS = (
    ('Suspended', 'Suspended'),
    ('Current', 'Currrent'),
    ('Active', 'Active'),
)

PROFORMA = (
    ('Pending', 'Pending'),
    ('Quotation', 'Quotation'),
    ('Active', 'Active'),
)

QUOTESTAT = (
    ('Pending', 'Pending'),
    ('Submitted', 'Submitted'),
    ('Counter Offer', 'Counter Offer'),
    ('Success', 'Success'),
)

PLAYERSTATUS = (
    ('None', 'None'),
    ('Done', 'Done'),
)

INVOICESTAT = (
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
    ('Cancelled', 'Cancelled'),
)

UNIT = (
    ('Tonnes', 'Metric Tonnes'),
    ('Ounces', 'Ounces'),
    ('Kgs', 'Kgs'),
)

GRADEUNIT = (
    ('Kgs/Tonne', 'Kgs Per Tonne'),
    ('Grams/Tonne', 'Grams Per Tonne'),
    ('Ounces/Tonne', 'Ounces Per Tonne'),
    ('%', '%'),
)

MATERIAL = (
    ('Ore', 'Ore'),
    ('Waste', 'Waste'),
    ('Mineral', 'Mineral'),
)

SUB = (
    ('Subs', 'Subs'),
    ('On boarding', 'On boarding'),
    ('Fees', ' Fees'),
)

PURPOSE = (
    ('Mine-Owner', 'Mine-Owner'),
    ('Investor', 'Investor'),
    ('Service Provider', 'Service Provider'),
)

PERIOD = (
    ('Week', 'Week'),
    ('Month', 'Month'),
    ('Quarter', 'Quarter'),
    ('Annual', 'Annual'),
)


SUBTYPE = (
    ('Mine Owner', 'Mine Owner'),
    ('Investor', 'Investor'),
    ('Service Provider', 'Service Provider'),
    ('Combination', 'Combination'),
)


SUBPERIOD = (
    ('Quarter', 'Quarter'),
    ('Bi-Annual', 'Bi-Annual'),
    ('Annual', 'Annual'),
)

class Country(models.Model):
    country = models.CharField(max_length=100)
    nationality = models.CharField(max_length=30, default='Zimbabwe')
    geom = models.PolygonField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        self_nationality = str(self.nationality)
        return self_nationality


class Rates(models.Model):
    purpose = models.CharField(max_length=100, choices=PURPOSE)
    sub = models.CharField(max_length=30, choices=SUB)
    amount = models.FloatField()
    period = models.CharField(max_length=30, choices=PERIOD)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class IndRecord(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=6, choices=SEX)
    dob = models.DateField(verbose_name='Date of Birth')
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    nid = models.CharField(max_length=50, null=False, verbose_name='Identity Number')
    status = models.CharField(max_length=10, choices=PLAYERSTATUS, default='None')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        first_name = str(self.first_name)
        last_name = str(self.last_name)
        return first_name + " " + last_name


class CorpRecord(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=CORPTYPE)
    doi = models.DateField(verbose_name='Date of Inc')
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=50, null=False, verbose_name='Identity Number')
    agents = models.ManyToManyField(User, through='CorpAgentRelation', related_name='agent_user')
    status = models.CharField(max_length=10, choices=PLAYERSTATUS, default='None')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.name)
        reg_number = str(self.reg_number)
        return name + reg_number


class Syndicate(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=100)
    dor = models.DateField(verbose_name='Date of Creation')
    members = models.ManyToManyField(IndRecord, through='SyndMemberRelation')
    agents = models.ManyToManyField(User, through='SyndAgentRelation', related_name='syndicate_agent_user')
    status = models.CharField(max_length=10, choices=PLAYERSTATUS, default='None')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SyndMemberRelation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    syndicate = models.ForeignKey(Syndicate, on_delete=models.CASCADE)
    member = models.ForeignKey(IndRecord, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=MEMBERSTATUS, default='Current')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class CorpAgentRelation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    company = models.ForeignKey(CorpRecord, on_delete=models.CASCADE)
    agent = models.ForeignKey(IndRecord, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=MEMBERSTATUS, default='Current')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class SyndAgentRelation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    syndicate = models.ForeignKey(Syndicate, on_delete=models.CASCADE)
    agent = models.ForeignKey(IndRecord, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=MEMBERSTATUS, default='Current')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Player(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    type = models.CharField(max_length=30, choices=PLAYERS)
    ref = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField()
    email = models.EmailField(null=True)
    bank = models.CharField(max_length=100, null=True)
    bank_account = models.CharField(max_length=50, null=True)
    street_address = models.CharField(max_length=100)
    trxn_balance = models.FloatField(default=0)
    suburb = models.CharField(max_length=100, verbose_name='Surburb / Zip Code')
    city = models.CharField(max_length=100, verbose_name='Town / City')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Nationality')
    sub_type = models.CharField(max_length=16, choices=SUBTYPE, default='Mine Owner')
    sub_period = models.CharField(max_length=16, choices=SUBPERIOD, default='Quarter')
    sub_amount = models.FloatField(default=1)
    payment_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default='True')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlayerUserRelation(models.Model):

    STATUS = (
        ('Non Active', 'Non Active'),
        ('Active', 'Active'),
    )

    date_created = models.DateField(auto_now_add=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS, default='Active')
    investor = models.BooleanField(default=False)
    mine_owner = models.BooleanField(default=False)
    service_provider = models.BooleanField(default=False)
    internal = models.BooleanField(default=False)
    party = models.ForeignKey(User, on_delete=models.CASCADE)


class AffiliateOrgs(models.Model):
    organisation = models.CharField(max_length=100)


class Affiliations(models.Model):

    STATUS = (
        ('Non Active', 'Non Active'),
        ('Active', 'Active'),
    )

    date_created = models.DateField(auto_now_add=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS, default='Active')
    organisation = models.ForeignKey(AffiliateOrgs, on_delete=models.CASCADE)


class PlayerCertificates(models.Model):
    date_created = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=30, choices=PLAYERCERT)
    issue_date = models.DateField(null=True)
    pdf = models.FileField(upload_to='images/certificates/', null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        xtra = str(self.type)
        issue_date = str(self.issue_date)
        return xtra + " " + issue_date


class Mineral(models.Model):
    name = models.CharField(max_length=30, null=False)
    price = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DepositType(models.Model):
    name = models.CharField(max_length=30, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MiningClaim(models.Model):

    MINEATTACH = (
        ('None', 'None'),
        ('Attached', 'Attached'),
    )
    date_created = models.DateField(auto_now_add=True, null=True)
    reg_date = models.DateField(null=False)
    name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=50, choices=MINECLAIM)
    reg_number = models.CharField(max_length=20, null=False)
    area = models.FloatField(blank=True)
    status = models.CharField(max_length=30, choices=OWNERSTATUS, default='Current', null=True)
    mine_attach = models.CharField(max_length=30, choices=MINEATTACH, default='None', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def attach(self):
        if MineClaimRelation.objects.filter(claim=self):
            attach = MineClaimRelation.objects.filter(claim=self).last().status
        else:
            attach = 'None'
        return attach

    def __str__(self):
        return self.name


class MiningClaimLocation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(MiningClaim, on_delete=models.CASCADE)
    location = models.PointField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def lat_long(self):
        return list(getattr(self.location, 'coords', [])[::-1])

    def __str__(self):
        return self.name.name


class MiningClaimBeacons(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(MiningClaim, on_delete=models.CASCADE)
    location = models.MultiPointField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def lat_long(self):
        return list(getattr(self.location, 'coords', [])[::-1])

    def __str__(self):
        return self.name.name


class Dummy(models.Model):
    location = models.CharField(max_length=2000, null=True)


class MiningClaimPolygon(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(MiningClaim, on_delete=models.CASCADE, null=True)
    location = models.PolygonField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def lat_long(self):
        return list(getattr(self.location, 'coords', [])[::-1])

    def __str__(self):
        return self.name.name


class Mine(models.Model):

    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=100, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    mineral = models.ManyToManyField(Mineral, through='MineMineral')
    insp_date = models.DateField(null=False, verbose_name='Last Inspected')
    insp_status = models.CharField(max_length=20, choices=OWNERSTATUS, default="Free")
    resource_type = models.ForeignKey(DepositType, on_delete=models.CASCADE)
    reserves_proven = models.IntegerField(null=True)
    reserves_possible = models.IntegerField(null=True)
    reserves_probable = models.IntegerField(null=True)
    claim = models.ManyToManyField(MiningClaim, through='MineClaimRelation')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MineLocation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(Mine, on_delete=models.CASCADE, related_name='mine_locations')
    location = models.PointField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def lat_long(self):
        return list(getattr(self.location, 'coords', [])[::-1])

    def __str__(self):
        return self.name.name


class MinePolygon(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(Mine, on_delete=models.CASCADE)
    polygon = models.MultiPolygonField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def lat_long(self):
        return str(self.polygon.coords)
        # return [[point.lat, point.lon] for point in self.polygon]

    def __str__(self):
        return self.name.name


class MineOwnerRelation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=OWNERSTATUS, default='Current')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        mine = str(self.mine)
        owner = str(self.owner)
        return mine + " " + owner


class MineInvestReq(models.Model):
    STATUS = (
        ('Free', 'Free'),
        ('Cart', 'Cart'),
        ('Field', 'Field'),
        ('Mandate', 'Mandate'),
        ('Un-Available', 'Un-Available'),
    )
    date_created = models.DateField(auto_now_add=True, null=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    invest_type = models.CharField(max_length=100, choices=INVESTYPE)
    value = models.FloatField()
    conglomerate = models.BooleanField(default=False)
    valid = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default="Free", null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        mine = str(self.mine)
        status = str(self.status)
        return mine + " " + status


class MineClaimRelation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    claim = models.ForeignKey(MiningClaim, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=OWNERSTATUS, default='Current')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class MineMineral(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    mineral = models.ForeignKey(Mineral, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class MineJobList(models.Model):
    job = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.job)


class MineEmployees(models.Model):

    MINEPOSTS = (
        ('Chief', 'Chief'),
        ('Snr', 'Senior'),
        ('Ass', 'Assistant'),
        ('Jnr', 'Juniour'),
        ('Snr', 'Senior'),
        ('Skilled', 'Skilled'),
        ('Semi Skilled', 'Semi Skilled'),
    )

    date_created = models.DateField(auto_now_add=True, null=True)
    date_employed = models.DateField(null=True)
    employee = models.ForeignKey(IndRecord, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(MineJobList, on_delete=models.CASCADE)
    post = models.CharField(max_length=30, choices=MINEPOSTS)
    pdf = models.FileField(upload_to='docs/', blank=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class MineCertificates(models.Model):
    date_created = models.DateField(auto_now_add=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=MINECERTIFICATES)
    issue_date = models.DateField(null=True)
    pdf = models.ImageField(upload_to='images/certificates/', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        mine = str(self.mine)
        issue_date = str(self.issue_date)
        return mine + " " + str(self.type) + " " + issue_date


class MineReports(models.Model):
    date_created = models.DateField(auto_now_add=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=MINEREPORTS)
    report_date = models.DateField(null=True)
    pdf = models.FileField(upload_to='docs/', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.mine)
        xtra = str(self.type)
        report_date = str(self.report_date)
        return name + " " + xtra + " " + report_date


class MineAgreements(models.Model):
    date_created = models.DateField(auto_now_add=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE, blank=True)
    type = models.CharField(max_length=50, choices=MINEAGREEMENTS)
    counter_party = models.CharField(max_length=100)
    report_date = models.DateField(null=True)
    pdf = models.FileField(upload_to='docs/', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.mine) + " "
        xtra = str(self.type)
        report_date = str(self.report_date)
        if self.mine:
            return name + xtra + " " + report_date
        else:
            return xtra + " " + report_date


class MineReceipts(models.Model):
    date_created = models.DateField(auto_now_add=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE, blank=True)
    type = models.CharField(max_length=50, choices=MINERECEIPTS)
    report_date = models.DateField(null=True)
    rec_number = models.IntegerField()
    pdf = models.FileField(upload_to='docs/', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.mine)
        xtra = str(self.type)
        rec_no = str(self.rec_number)
        report_date = str(self.report_date)
        return "Receipt Number" + xtra + " " + rec_no + " " + report_date


class MineLetters(models.Model):

    INOUT = (
        ('In', 'In'),
        ('Out', 'Out'),
    )
    date_created = models.DateField(auto_now_add=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE, blank=True)
    type = models.CharField(max_length=50, choices=MINELETTERS)
    report_date = models.DateField(null=True)
    other_party = models.CharField(max_length=100)
    subject = models.CharField(max_length=500)
    inout = models.CharField(max_length=4, choices=INOUT)
    pdf = models.FileField(upload_to='docs/', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.mine)
        party = str(self.other_party)
        inout = str(self.type)
        report_date = str(self.report_date)
        if inout == "In":
            return "From" + " " + party + " " + report_date
        else:
            return "To" + " " + party + " " + report_date


class OtherDocs(models.Model):
    date_created = models.DateField(auto_now_add=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE, blank=True)
    report_date = models.DateField(null=True)
    subject = models.CharField(max_length=500)
    pdf = models.FileField(upload_to='docs/', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        xtra = str(self.subject)[:50]
        report_date = str(self.report_date)
        return xtra + " " + report_date


class MineProduction(models.Model):
    date_created = models.DateField(auto_now_add=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    material = models.CharField(max_length=25, choices=MATERIAL)
    mineral = models.ForeignKey(Mineral, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.FloatField()
    unit = models.CharField(max_length=30, choices=UNIT)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.mine)
        material = str(self.material)
        return name + " " + material + " " + str(self.quantity)


class WorksList(models.Model):
    works = models.CharField(max_length=50)

    def __str__(self):
        return self.works


class MineWorks(models.Model):
    date_created = models.DateField(auto_now_add=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    works = models.ForeignKey(WorksList, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    comment = models.CharField(max_length=255, null=True, blank=True)
    location = models.MultiPointField(blank=True, null=True)
    polygon = models.PolygonField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.mine)
        works = str(self.works)
        return name + " " + works

    @property
    def lat_long(self):
        return list(getattr(self.location, 'coords', [])[::-1])


class PlantList(models.Model):
    plant = models.CharField(max_length=50)

    def __str__(self):
        return self.plant


class MinePlant(models.Model):
    date_created = models.DateField(auto_now_add=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    plant = models.ForeignKey(PlantList, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    comment = models.CharField(max_length=255, null=True, blank=True)
    location = models.PointField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.mine)
        plant = str(self.plant)
        return name + " " + plant


class YellowList(models.Model):
    plant = models.CharField(max_length=50)

    def __str__(self):
        return self.plant


class MineYellowPlant(models.Model):
    date_created = models.DateField(auto_now_add=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    plant = models.ForeignKey(YellowList, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    comment = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.mine)
        plant = str(self.plant)
        return name + " " + plant


class MineLabour(models.Model):
    date_created = models.DateField(auto_now_add=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    management = models.IntegerField()
    skilled = models.IntegerField()
    semi_skilled = models.IntegerField()
    unskilled = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def staff(self):
        staff = 0
        staff_list = [self.skilled, self.semi_skilled, self.unskilled, self.management]
        for item in staff_list:
            staff += item
            return staff

    def __str__(self):
        name = str(self.mine)
        staff = str(self.staff)
        return name + " " + staff


class ClaimRegCert(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    issue_date = models.DateField(null=True)
    pdf = models.ImageField(upload_to='images/certificates/', null=True)
    claim = models.ForeignKey(MiningClaim, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.claim)
        return name + " " + "Reg Certificate"


class Beacon(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    mining_claim = models.ForeignKey(MiningClaim, on_delete=models.CASCADE)
    symbol = models.IntegerField(null=True, default=0)
    latitude = models.FloatField()
    longitude = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def lat_long(self):
        return [self.latitude, self.longitude]

    def __str__(self):
        name = str(self.mining_claim)
        return name + " " + "Beacon" + " " + str(self.symbol)


class Investor(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        player = str(self.player)
        return player


class InvestorMineRelation(models.Model):

    STATUS = (
        ('Cart', 'Cart'),
        ('Mandate-Request', 'Mandate-Request'),
        ('Mandate', 'Mandate'),
        ('Free', 'Free'),
    )
    date_created = models.DateField(auto_now_add=True, null=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS, default='Cart')
    valid = models.DateField(null=True)

    def __str__(self):
        investor = str(self.investor)
        mine = str(self.mine)
        status = str(self.status)
        return investor + " " + mine + " " + status


class CartRequest(models.Model):

    date_created = models.DateField(auto_now_add=True, null=True)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    valid = models.DateTimeField()
    mineral = models.ForeignKey(Mineral, on_delete=models.CASCADE)
    deposit_type = models.ManyToManyField(DepositType)
    resource_unit = models.CharField(max_length=30, choices=UNIT)
    min_grade = models.IntegerField()
    grade_unit = models.CharField(max_length=30, choices=GRADEUNIT)
    invest_type = models.CharField(max_length=30, choices=INVESTYPE)
    location = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    polygon = models.PolygonField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        investor = str(self.investor)
        ref = str(self.id)
        return investor + " " + "Cart Request" + " " + ref


class CartMineMatch(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    cart_request = models.ForeignKey(CartRequest, on_delete=models.CASCADE)
    mines = models.ManyToManyField(Mine, through='CartMineRelation')
    valid = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        request = str(self.cart_request)
        xtra = str(self.id)
        return request + " " + "Match" + " " + xtra


class CartMineRelation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    cart = models.ForeignKey(CartMineMatch, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        cart = str(self.cart)
        mine = str(self.mine)
        return cart + " " + mine


class MandateTypeList(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class MandateRequest(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    cart_mine_match = models.ForeignKey(CartMineMatch, on_delete=models.CASCADE)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    purpose = models.ForeignKey(MandateTypeList, on_delete=models.CASCADE)
    period = models.DateField()
    duration = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        xtra = str(self.id)
        return "Mandate Request" + " " + xtra


class MineMandateRequest(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Proforma', 'Proforma'),
        ('Mandate', 'Mandate'),
        ('Failed', 'Failed'),
        ('Complete', 'Complete'),
    )
    date_created = models.DateField(auto_now_add=True, null=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    mandate_request = models.ForeignKey(MandateRequest, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS, default='Pending')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        mandate = str(self.mandate_request)
        return mandate


class MandateProforma(models.Model):

    PROFORMASTAT = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    )
    date_created = models.DateField(auto_now_add=True, null=True)
    mandate_request = models.ForeignKey(MandateRequest, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(null=True)
    status = models.CharField(max_length=15, choices=PROFORMASTAT, default='Pending')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Mandate(models.Model):

    date_created = models.DateField(auto_now_add=True, null=True)
    mandate_request = models.ForeignKey(MandateRequest, on_delete=models.CASCADE)
    valid = models.DateField()
    mine = models.ManyToManyField(Mine, through='MineMandateRelation')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        xtra = str(self.id)
        return "Mandate" + " " + xtra


class MineMandateRelation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        mine = str(self.mine)
        status = str(self.mandate)
        return mine + " " + status


class ProfService(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ServiceProvRole(models.Model):
    name = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    """
    RATING = (
        ('Professional', 'Professional'),
        ('Senior', 'Senior'),
        ('Junior', 'Junior'),
        ('Student', 'Student'),
        ('Graduate', 'Graduate'),
        ('Skilled', 'Skilled'),
        ('Semi-Skilled', 'Semi-Skilled'),
        ('Labourer', 'Labourer'),
    )
    """


class FieldReq(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Service Choice', 'Service Choice'),
        ('Proforma', 'Proforma'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
        ('Approved', 'Approved'),
        ('Field', 'Field')
    )

    date_created = models.DateField(auto_now_add=True, null=True)
    mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE)
    service = models.ForeignKey(ProfService, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000, blank=True)
    pdf = models.FileField(upload_to='docs/', null=True)
    period = models.DateTimeField()
    service_req = models.BooleanField(verbose_name='Service Providers Required?')
    provider_roles = models.ManyToManyField(ServiceProvRole, through='ServiceProvRequired')
    status = models.CharField(max_length=15, choices=STATUS, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        service = str(self.service)
        period = str(self.id)
        return service + " " + period


class ServiceProvRequired(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )
    field_request = models.ForeignKey(FieldReq, on_delete=models.CASCADE, null=True)
    provider_role = models.ForeignKey(ServiceProvRole, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=15, choices=STATUS, null=True, default='Pending')

    def __str__(self):
        xtra = str(self.id)
        role = str(self.provider_role)
        quantity = str(self.quantity)
        return xtra + " " + quantity + " " + role


class FieldCostList(models.Model):
    cost_type = models.CharField(max_length=100)

    def __str__(self):
        cost_type = str(self.cost_type)
        return cost_type


class AdminPremium(models.Model):
    service = models.ForeignKey(ProfService, on_delete=models.DO_NOTHING)
    premium = models.FloatField()

    def __str__(self):
        service = str(self.service)
        return service


class FieldSupCosts(models.Model):
    TYPE = (
        ('Budget', 'Budget'),
        ('Final', 'Final')
    )
    field_request = models.ForeignKey(FieldReq, on_delete=models.CASCADE, null=True)
    cost_type = models.ForeignKey(FieldCostList, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True)
    cost = models.FloatField()
    final = models.FloatField(blank=True, null=True)

    def __str__(self):
        cost_type = str(self.cost_type)
        cost = str(self.cost)
        return cost_type + " " + cost


class ServiceProv(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(Player, on_delete=models.CASCADE, null=False)
    service = models.ForeignKey(ProfService, on_delete=models.CASCADE, null=False)
    rating = models.ForeignKey(ServiceProvRole, on_delete=models.CASCADE)
    summary = models.TextField(max_length=3000, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        name = str(self.name)
        return name


class SerProvProfile(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(ServiceProv, on_delete=models.CASCADE, null=False)
    principal = models.CharField(max_length=100, blank=True)
    """Principal means the Employer or Investor"""
    title = models.CharField(max_length=255)
    role = models.ForeignKey(ServiceProvRole, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField(blank=True)
    description = models.CharField(max_length=1000)
    reference = models.CharField(max_length=100, blank=True)
    """reference means the represantative of the Employer or Investor"""
    ref_contact = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class WorkHistAttach(models.Model):
    TYPE = (
        ('Contract', 'Contract'),
        ('Letter', 'Letter'),
        ('Invoice', 'Invoice'),
        ('Plan', 'Plan'),
        ('Report', 'Report'),
    )
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(ServiceProv, on_delete=models.CASCADE, null=False)
    type = models.CharField(max_length=30, choices=TYPE)
    pdf = models.FileField(upload_to='docs/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class FieldProforma(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    field_request = models.ForeignKey(FieldReq, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=PROFORMA, default='Pending', null=True)
    provider_costs = models.FloatField(default=0)
    support_costs = models.FloatField(default=0)
    admin_premium = models.ForeignKey(AdminPremium, on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        field_request = str(self.field_request)
        return field_request


class FieldProviderQuote(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    service_ref = models.ForeignKey(ServiceProvRequired, on_delete=models.CASCADE, null=True)
    provider = models.ForeignKey(ServiceProv, on_delete=models.CASCADE)
    cost = models.FloatField()
    counter_offer = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=1055, blank=True)
    pdf = models.ImageField(upload_to='docs/', blank=True)
    status = models.CharField(max_length=15, choices=QUOTESTAT, default='Pending')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        request = str(self.id)
        provider = str(self.provider)
        status = str(self.status)
        return "Quote" + request + " " + provider + " " + status


class FieldReqWinQte(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    service_ref = models.ForeignKey(ServiceProvRequired, on_delete=models.CASCADE, null=True)
    quote = models.ForeignKey(FieldProviderQuote, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        quote = str(self.quote_id)
        service_ref = str(self.service_ref_id)
        return "Quote : " + quote + " " + "Service Ref : " + service_ref


class Field(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Under-Way', 'Under-Way'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    )

    date_created = models.DateField(auto_now_add=True, null=True)
    proforma = models.ForeignKey(FieldProforma, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    task = models.TextField(max_length=2000)
    from_date = models.DateField()
    to_date = models.DateField()
    provider = models.ManyToManyField(ServiceProv, through='FiedlProviderRelation')
    mine_owner_requirements = models.ManyToManyField(MineJobList, through='FiedlMineRequirements', blank=True)
    """Mine owner requirements means the Mine Employees required for purposes of assisting with the field visit"""
    status = models.CharField(max_length=15, choices=STATUS, default='Pending')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def detail(self):
        detail = Urls.objects.filter(url='field_activity_detail.html').last()
        return detail

    def __str__(self):
        return "Field Activity" + " " + str(self.id) + " " + str(self.subject)


class FiedlProviderRelation(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    provider = models.ForeignKey(ServiceProv, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        field = str(self.field)
        provider = str(self.provider)
        return field + " " + provider


class FiedlMineRequirements(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    required = models.ForeignKey(MineJobList, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        required = str(self.required.job)
        return required


class TrxnPurpose(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    """
    ['Mandate Invoice', 'Field Invoice', 'Subs', 'Reversal']
    """


class Trxns(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    payer = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    payee = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='trxns_payee')
    amount = models.FloatField(null=True)
    reverse_trxn = models.IntegerField(null=True, blank=True)
    invoice_ref = models.IntegerField(default=0, null=True)
    purpose = models.ForeignKey(TrxnPurpose, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        xtra = str(self.id)
        return "Transaction" + " " + xtra


class Invoice(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    mandate_request = models.ForeignKey(MandateRequest, on_delete=models.CASCADE, null=True, blank=True)
    mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE, null=True, blank=True)
    field_request = models.ForeignKey(FieldReq, on_delete=models.CASCADE, null=True, blank=True)
    payer = models.ForeignKey(Player, on_delete=models.CASCADE, null=False)
    amount = models.FloatField()
    purpose = models.ForeignKey(TrxnPurpose, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=15, choices=INVOICESTAT, default='Pending')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        xtra = str(self.id)
        return "Invoice" + " " + xtra


class Receipt(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=False)
    trxn_ref = models.ForeignKey(Trxns, on_delete=models.CASCADE, null=False)
    amount = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Receipt" + " " + self.id


class FieldInvoice(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=False)
    field_proforma = models.ForeignKey(FieldProforma, on_delete=models.CASCADE,
                                       null=False, related_name='invoice_proforma')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Field Invoice" + " " + str(self.id)


class FieldActivityQoutes(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Supplied Quote', 'Supplied Quote'),
        ('Winning', 'Winning'),
    )
    date_created = models.DateField(auto_now_add=True)
    activity = models.ForeignKey(Field, on_delete=models.CASCADE, null=True)
    service_provider = models.ForeignKey(ServiceProv, on_delete=models.CASCADE,
                                         null=True, related_name='invoice_proforma')
    amount = models.FloatField(null=True)
    status = models.CharField(max_length=15, choices=STATUS, default='Pending', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        activity = str(self.activity.id)
        provider = str(self.service_provider)
        return activity + " " + provider


class FieldAttachments(models.Model):

    TYPE = (
        ('Technical', 'Technical'),
        ('Receipts', 'Receipts'),
    )
    date_created = models.DateField(auto_now_add=True, null=True)
    activity = models.ForeignKey(Field, on_delete=models.CASCADE, null=False)
    type = models.CharField(max_length=15, choices=TYPE)
    name = models.CharField(max_length=30)
    pdf = models.FileField(upload_to='docs/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        activity = str(self.activity.id)
        xtra = str(self.type)
        name = str(self.name)
        return activity + " " + " " + xtra + " " + name


class FieldAcquit(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    activity = models.ForeignKey(Field, on_delete=models.CASCADE, null=True)
    acquit = models.BooleanField(null=True, default='False')
    comment = models.TextField(max_length=2000,verbose_name='Task Report', default='Complete')
    recommendation = models.TextField(max_length=2000, blank=True, verbose_name='Mine Recommendation')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def player(self):
        player = PlayerUserRelation.objects.filter(party=self.author).last().player
        return player


class Alerts(models.Model):

    TYPE = (
        ('Active', 'Active'),
        ('Off', 'Off'),
    )
    date_created = models.DateField(auto_now_add=True, null=True)
    message = models.CharField(max_length=255, null=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=15, choices=TYPE, default='Active')

    def __str__(self):
        return self.message


class TemplateLinks(models.Model):
    name = models.CharField(max_length=255)


class ServerIP(models.Model):
    name = models.CharField(max_length=255)


class PlayerCash(models.Model):

    TYPE = (
        ('In', 'In'),
        ('Out', 'Out'),
    )
    date_created = models.DateField(auto_now_add=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    type = models.CharField(max_length=15, choices=TYPE)
    ref = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        player = str(self.player)
        xtra = str(self.type)
        return "Cash" + " " + xtra + " " + player + " " + str(self.amount)