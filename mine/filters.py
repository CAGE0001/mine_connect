import django_filters
from django_filters.widgets import RangeWidget
from django_filters import DateFilter
from .models import *
from datetime import timedelta, timezone, date


MINECLAIM = (
    ('PMB', 'Precious Metal'),
    ('BMB', 'Base Metal'),
    ('SG', 'Special Grant'),
    ('SB', 'Special Block')
)

PLAYERS = (
    ('Individual', 'Individual'),
    ('Corporate', 'Corporate'),
    ('Syndicate', 'Syndicate'),
)


def filter_by_range(queryset, name, value):
        start = value.start
        end = value.stop
        if end == None:
            end = date.today()
        return queryset.filter(name__gte=start, name__lte=end)


class IndiRecordFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', label='First Name')
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='Last Name')
    nid = django_filters.CharFilter(lookup_expr='iexact', label='Identity Number')
    nationality = django_filters.CharFilter(field_name='nationality__nationality', lookup_expr='iexact')

    on_board = django_filters.DateFromToRangeFilter(
        label='On Board Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Of Birth:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = IndRecord
        fields = ('__all__', 'on_board', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, dob__gte, dob__lte):
        pass


class CorpRecordFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Company Name')
    reg_number = django_filters.CharFilter(lookup_expr='iexact', label='Registration Number')
    type = django_filters.ChoiceFilter(choices=CORPTYPE, label='Company Type')
    nationality = django_filters.CharFilter(field_name='nationality__nationality', lookup_expr='iexact')

    on_board = django_filters.DateFromToRangeFilter(
        label='On Board Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Incorporated:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = CorpRecord
        fields = ('__all__', 'on_board', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, doi__gte, doi__lte):
        pass


class SyndRecordFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Syndicate Name')

    on_board = django_filters.DateFromToRangeFilter(
        label='On Board Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Registered:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Syndicate
        fields = ('__all__', 'on_board','date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, dor__gte, dor__lte):
        pass


class MineFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Mine Name')
    owner = django_filters.CharFilter(lookup_expr='icontains', label='Mine Owner')
    mineral = django_filters.CharFilter(lookup_expr='icontains', label='Mineral')

    class meta:
        model = Mine
        fields = '__all__'


class PlayerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Entity Name')
    bank = django_filters.CharFilter(lookup_expr='icontains', label='bank')
    country = django_filters.CharFilter(field_name='nationality__country', lookup_expr='iexact', label='Country')
    type = django_filters.ChoiceFilter(choices=PLAYERS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Player
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MoreProductionFilter(django_filters.FilterSet):
    mineral = django_filters.ModelChoiceFilter(queryset=Mineral.objects.all(), label='Mineral')
    mineral = django_filters.CharFilter(field_name='mineral__name', lookup_expr='iexact')
    nid = django_filters.CharFilter(lookup_expr='icontains', label='Identity Ref')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Started:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_end = django_filters.DateFromToRangeFilter(
        label='Date Ended:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineProduction
        fields = ('__all__', 'date_range', 'date_end')

    def filter(self, start_date__gte, start_date__lte):
        pass

    def filter1(self, end_date__gte, end_date__lte):
        pass


class PlayerIndFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', label='First Name')
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='Surname')
    nid = django_filters.CharFilter(lookup_expr='icontains', label='Identity Ref')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = IndRecord
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class PlayerCorpFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    reg_number = django_filters.CharFilter(lookup_expr='icontains', label='Identity Ref')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = CorpRecord
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class PlayerSyndFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='First Name')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Syndicate
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineClaimsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Claim Name')
    type = django_filters.ChoiceFilter(choices=MINECLAIM)

    class meta:
        model = MiningClaim
        fields = '__all__'


class ClaimsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Claim Name')
    type = django_filters.ChoiceFilter(choices=MINECLAIM)
    mine = django_filters.CharFilter(lookup_expr='icontains', label='Mine Name')
    reg_number = django_filters.CharFilter(lookup_expr='icontains', label='Registration Number')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )
    reg_date_range = django_filters.DateFromToRangeFilter(
        label='Registration Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MiningClaim
        fields = ('__all__', 'date_range', 'reg_date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, reg_date__gte, reg_date__lte):
        pass


class FieldFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label='Field Activity Ref')
    subject = django_filters.CharFilter(lookup_expr='icontains', label='Activity')
    proforma = django_filters.CharFilter(field_name='proforma__field_request__mandate__mandate_request__cart_mine_match__cart_request__investor__player__name', lookup_expr='iexact', label='Investor')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )
    reg_date_range = django_filters.DateFromToRangeFilter(
        label='Starting Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Field
        fields = ('__all__', 'date_range', 'reg_date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, from_date__gte, from_date__lte):
        pass


class ServiceFieldFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label='Field Activity Ref')
    subject = django_filters.CharFilter(lookup_expr='icontains', label='Activity')
    proforma = django_filters.CharFilter(field_name='proforma__field_request__mandate__mandate_request__cart_mine_match__cart_request__investor__player__name', lookup_expr='iexact', label='Investor')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )
    reg_date_range = django_filters.DateFromToRangeFilter(
        label='Starting Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Field
        fields = ('__all__', 'date_range', 'reg_date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, from_date__gte, from_date__lte):
        pass


class ServiceQuoteFilter(django_filters.FilterSet):

    STATUS = (
        ('Pending', 'Pending'),
        ('Supplied Quote', 'Supplied Quote'),
        ('Winning', 'Winning'),
    )

    id = django_filters.NumberFilter(label='Quotation Ref')
    provider = django_filters.CharFilter(field_name='provider__name__player__name', lookup_expr='iexact', label='Service Provider')
    status = django_filters.ChoiceFilter(choices=STATUS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = FieldProviderQuote
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class ServiceReqFilter(django_filters.FilterSet):
    field_request = django_filters.NumberFilter(field_name='provider__id', lookup_expr='exact', label='Field Request Ref')

    class meta:
        model = ServiceProvRequired
        fields = '__all__'


class ProviderQuoteFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(label='Quotation Ref')
    status = django_filters.ChoiceFilter(choices=QUOTESTAT)
    cost = django_filters.NumberFilter(lookup_expr='exact', label='Quote amount')
    counter_offer = django_filters.NumberFilter(lookup_expr='exact', label='Quote Counter Offer')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = FieldProviderQuote
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class ServiceChoiceFilter(django_filters.FilterSet):

    rating = django_filters.CharFilter(field_name='rating__name', lookup_expr='iexact', label='Professional Rating')

    class meta:
        model = ServiceProv
        fields = '__all__'


class CashFilter(django_filters.FilterSet):

    STATUS = (
        ('In', 'In'),
        ('Out', 'Out'),
    )

    player = django_filters.CharFilter(field_name='player__name', lookup_expr='icontains', label='Service Provider')
    type = django_filters.ChoiceFilter(choices=STATUS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = PlayerCash
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class ServiceAttachFilter(django_filters.FilterSet):

    STATUS = (
        ('Pending', 'Pending'),
        ('Supplied Quote', 'Supplied Quote'),
        ('Winning', 'Winning'),
    )

    # activity = django_filters.ChoiceFilter(field_name='activity__provider', lookup_expr='icontains', label='Service Provider')
    status = django_filters.ChoiceFilter(choices=STATUS)

    class meta:
        model = FieldAttachments
        fields = '__all__'


class MineEmployeesFilter(django_filters.FilterSet):

    MINEPOSTS = (
        ('Chief', 'Chief'),
        ('Snr', 'Senior'),
        ('Ass', 'Assistant'),
        ('Jnr', 'Juniour'),
        ('Snr', 'Senior'),
        ('Skilled', 'Skilled'),
        ('Semi Skilled', 'Semi Skilled'),
    )

    id = django_filters.NumberFilter(label='Employee Ref')
    employee = django_filters.CharFilter(field_name='employee', lookup_expr='icontains', label='Individual')
    mine = django_filters.CharFilter(field_name='mine__name', lookup_expr='icontains', label='Mine')
    # mine = django_filters.ModelChoiceFilter(queryset=Mine.objects.all(), label='Mine')
    job = django_filters.ModelChoiceFilter(queryset=MineJobList.objects.all(), label='Job description')
    post = django_filters.ChoiceFilter(choices=MINEPOSTS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineEmployees
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class TrxnsFilter(django_filters.FilterSet):

    PURPOSE = (
        ('Mandate Invoice', 'Mandate Invoice'),
        ('Field Invoice', 'Field Invoice'),
        ('Subs', 'Subs'),
        ('Reversal', 'Reversal'),
    )

    id = django_filters.NumberFilter(label='Trxn Number')
    payer = django_filters.CharFilter(field_name='payer__name', lookup_expr='icontains', label='Paid By')
    payee = django_filters.CharFilter(field_name='payee__name', lookup_expr='icontains', label='Paid To')
    invoice_ref = django_filters.NumberFilter(label='Invoice Number')
    purpose = django_filters.ChoiceFilter(choices=PURPOSE)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Trxns
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class TrxFilter(django_filters.FilterSet):

    PURPOSE = (
        ('Mandate Invoice', 'Mandate Invoice'),
        ('Field Invoice', 'Field Invoice'),
        ('Subs', 'Subs'),
        ('Reversal', 'Reversal'),
    )

    id = django_filters.NumberFilter(label='Trxn Number')
    invoice_ref = django_filters.NumberFilter(label='Invoice Number')
    purpose = django_filters.ChoiceFilter(choices=PURPOSE)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Trxns
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineReportFilter(django_filters.FilterSet):

    mine = django_filters.CharFilter(field_name='mine__name', lookup_expr='icontains', label='Mine')
    type = django_filters.ChoiceFilter(choices=MINEREPORTS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineReports
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class FieldProviderQuoteFilter(django_filters.FilterSet):

    service_ref = django_filters.CharFilter(field_name='service_ref__provider_role__name', lookup_expr='icontains', label='Service')
    # service_ref = django_filters.ModelChoiceFilter(queryset=ServiceProvRequired.objects.all(), label='Services')
    # provider = django_filters.ModelChoiceFilter(queryset=ServiceProv.objects.all(), label='Service Provider')
    status = django_filters.ChoiceFilter(choices=QUOTESTAT)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = FieldProviderQuote
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class InvoiceOwnerFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(label='Invoice Ref')
    date_range = django_filters.DateFromToRangeFilter(
        label='Invoice Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Invoice
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineOwnerReportFilter(django_filters.FilterSet):

    type = django_filters.ChoiceFilter(choices=MINEREPORTS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineReports
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineOwnerCertificateFilter(django_filters.FilterSet):

    type = django_filters.ChoiceFilter(choices=MINECERTIFICATES)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineCertificates
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineCertificateFilter(django_filters.FilterSet):

    # mine = django_filters.ModelChoiceFilter(queryset=Mine.objects.all(), label='Mine')
    mine = django_filters.CharFilter(field_name='mine__name', lookup_expr='icontains', label='Mine')
    type = django_filters.ChoiceFilter(choices=MINECERTIFICATES)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineCertificates
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class ClaimRegFilter(django_filters.FilterSet):

    claim = django_filters.ModelChoiceFilter(queryset=MiningClaim.objects.all(), label='Mining Claim')
    claim = django_filters.CharFilter(field_name='claim', lookup_expr='icontains', label='Mining Claim')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = ClaimRegCert
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class ServiceProvFilter(django_filters.FilterSet):

    # name = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), label='Service Provider')
    name = django_filters.CharFilter(field_name='name__name', lookup_expr='iexact', label='Service Provider')
    # service = django_filters.ModelChoiceFilter(queryset=ProfService.objects.all(), label='Service')
    service = django_filters.CharFilter(field_name='service__name', lookup_expr='iexact', label='Service')
    # rating = django_filters.ModelChoiceFilter(queryset=ServiceProvRole.objects.all(), label='Rating')
    rating = django_filters.CharFilter(field_name='rating__name', lookup_expr='iexact', label='Professional Rating')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = ServiceProv
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineOwnerFilter(django_filters.FilterSet):
    # mine = django_filters.ModelChoiceFilter(queryset=Mine.objects.all(), label='Mine')
    mine = django_filters.CharFilter(field_name='mine__name', lookup_expr='iexact', label='Mine')
    # owner = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), label='Owner')
    owner = django_filters.CharFilter(field_name='owner__name', lookup_expr='iexact', label='Mine Owner')
    status = django_filters.ChoiceFilter(choices=OWNERSTATUS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineOwnerRelation
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MandateFilter(django_filters.FilterSet):

    STATUS = (
        ('Pending', 'Pending'),
        ('Under-Way', 'Under-Way'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
    )

    id = django_filters.NumberFilter(label='Mandate Ref')
    mandate_request = django_filters.ModelChoiceFilter(queryset=MandateRequest.objects.all(), label='Mandate Request')
    payment_status = django_filters.ChoiceFilter(choices=STATUS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )
    reg_date_range = django_filters.DateFromToRangeFilter(
        label='Registration Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Mandate
        fields = ('__all__', 'date_range', 'reg_date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, valid__gte, valid__lte):
        pass


class FieldProformaFilter(django_filters.FilterSet):

    STATUS = (
        ('Pending', 'Pending'),
        ('Under-Way', 'Under-Way'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
    )

    id = django_filters.NumberFilter(label='Proforma Ref')
    field_request = django_filters.ModelChoiceFilter(queryset=FieldReq.objects.all(), label='Field Request')
    status = django_filters.ChoiceFilter(choices=STATUS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = FieldProforma
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MandateRequestFilter(django_filters.FilterSet):
    STATUS = (
        ('Pending', 'Pending'),
        ('Proforma', 'Proforma'),
        ('Mandate', 'Mandate'),
        ('Failed', 'Failed'),
        ('Complete', 'Complete'),
    )

    id = django_filters.NumberFilter(label='Mandate Request Ref')
    cart_mine_match = django_filters.ModelChoiceFilter(queryset=CartMineMatch.objects.all(), label='Cart Match')
    purpose = django_filters.ModelChoiceFilter(queryset=MandateTypeList.objects.all(), label='Mandate Purpose')
    status = django_filters.ChoiceFilter(choices=STATUS, label='Status')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_valid = django_filters.DateFromToRangeFilter(
        label='Valid Until:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MandateRequest
        fields = ('__all__', 'date_range', 'date_valid')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, period_created__gte, period_created__lte):
        pass


class MandateRequestReadyFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(label='Mandate Request Ref')
    cart_mine_match = django_filters.ModelChoiceFilter(queryset=CartMineMatch.objects.all(), label='Cart Match')
    purpose = django_filters.ModelChoiceFilter(queryset=MandateTypeList.objects.all(), label='Mandate Purpose')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_valid = django_filters.DateFromToRangeFilter(
        label='Valid Until:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MandateRequest
        fields = ('__all__', 'date_range', 'date_valid')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, period_created__gte, period_created__lte):
        pass


class MandateProformaFilter(django_filters.FilterSet):

    PROFORMA = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    )

    id = django_filters.NumberFilter(label='Mandate Proforma Ref')
    mandate_request = django_filters.ModelChoiceFilter(queryset=MandateRequest.objects.all(), label='Mandate Request')
    status = django_filters.ChoiceFilter(choices=PROFORMA, label='Status')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MandateProforma
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class CartMineMatchFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(label='Cart Mine Ref')
    cart_request = django_filters.ModelChoiceFilter(queryset=CartRequest.objects.all(), label='Cart Request')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = CartMineMatch
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class InvestorFilter(django_filters.FilterSet):
    # player = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), label='Player')
    player = django_filters.CharFilter(field_name='player__name', lookup_expr='iexact', label='Player')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Investor
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class InvoiceFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(label='Invoice Number')
    # payer = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), label='Payer')
    payer = django_filters.CharFilter(field_name='payer__name', lookup_expr='iexact', label='Payer')
    purpose = django_filters.ModelChoiceFilter(queryset=TrxnPurpose.objects.all(), label='Purpose')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Invoice
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class ReceiptFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(label='Receipt Number')
    # invoice = django_filters.ModelChoiceFilter(queryset=Invoice.objects.all(), label='Invoice')
    invoice = django_filters.NumberFilter(field_name='invoice__id', lookup_expr='exact', label='Invoice Ref')
    # trxn_ref = django_filters.ModelChoiceFilter(queryset=Trxns.objects.all(), label='Trxn Ref')
    trxn_ref = django_filters.CharFilter(field_name='trxn_ref__id', lookup_expr='iexact', label='Trxn Ref')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Receipt
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class PlayerMineFilter(django_filters.FilterSet):
    STATUS = (
        ('Free', 'Free'),
        ('Cart', 'Cart'),
        ('Field', 'Field'),
        ('Mandate', 'Mandate'),
    )
    name = django_filters.CharFilter(lookup_expr='icontains', label='Mine Name')
    status = django_filters.ChoiceFilter(choices=STATUS)
    mineral = django_filters.CharFilter(lookup_expr='icontains', label='Mineral')
    reg_number = django_filters.CharFilter(lookup_expr='icontains', label='Registration Number')

    date_range = django_filters.DateFromToRangeFilter(
        label='Inspection date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Mine
        fields = ('__all__', 'date_range')

    def filter(self, insp_date__gte, insp_date__lte):
        pass


class MineMandateRequestFilter(django_filters.FilterSet):

    class meta:
        model = MineMandateRequest
        fields = '__all__'


class TrxnFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(label='Trxn Ref')
    # payer = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), label='Payer')
    # payer = django_filters.CharFilter(field_name='payer__name', lookup_expr='icontains', label='Payer')
    # payee = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), label='Payee')
    payee = django_filters.CharFilter(field_name='payee__name', lookup_expr='iexact', label='Payee')
    purpose = django_filters.ModelChoiceFilter(queryset=TrxnPurpose.objects.all(), label='Purpose')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Trxns
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineMandateRelationFilter(django_filters.FilterSet):

    class meta:
        model = MineMandateRelation
        fields = '__all__'


class CartMatchFilter(django_filters.FilterSet):

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = CartMineRelation
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MandateListFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label='Mandate Ref')
    mandate_request = django_filters.ModelChoiceFilter(queryset=MandateRequest.objects.all(), label='Mine')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_valid = django_filters.DateFromToRangeFilter(
        label='Valid Until:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = Mandate
        fields = ('__all__', 'date_range', 'date_valid')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, date_created__gte, date_created__lte):
        pass


class InvestorFieldReqFilter(django_filters.FilterSet):

    STATUS = (
        ('Pending', 'Pending'),
        ('Proforma', 'Proforma'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
        ('Approved', 'Approved'),
    )
    service = django_filters.ModelChoiceFilter(queryset=ProfService.objects.all(), label='Service')
    status = django_filters.ChoiceFilter(choices=STATUS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_valid = django_filters.DateFromToRangeFilter(
        label='Valid Until:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = FieldReq
        fields = ('__all__','date_range', 'date_valid')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, period__gte, period__lte):
        pass


class FieldReqFilter(django_filters.FilterSet):

    STATUS = (
        ('Pending', 'Pending'),
        ('Proforma', 'Proforma'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
        ('Approved', 'Approved'),
    )
    service = django_filters.ModelChoiceFilter(queryset=ProfService.objects.all(), label='Service')
    status = django_filters.ChoiceFilter(choices=STATUS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_valid = django_filters.DateFromToRangeFilter(
        label='Valid Until:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = FieldReq
        fields = ('__all__','date_range', 'date_valid')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, period__gte, period__lte):
        pass


class FieldReqReadyFilter(django_filters.FilterSet):

    service = django_filters.ModelChoiceFilter(queryset=ProfService.objects.all(), label='Payer')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    date_valid = django_filters.DateFromToRangeFilter(
        label='Valid Unti:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = FieldReq
        fields = ('__all__','date_range', 'date_valid')

    def filter(self, date_created__gte, date_created__lte):
        pass

    def filter1(self, period__gte, period__lte):
        pass


class InvestviewFieldReqFilter(django_filters.FilterSet):

    STATUS = (
        ('Pending', 'Pending'),
        ('Proforma', 'Proforma'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
        ('Approved', 'Approved'),
    )

    id = django_filters.NumberFilter(label='Field Request Ref')
    # mine = django_filters.ModelChoiceFilter(queryset=Mine.objects.all(), label='Mine')
    mine = django_filters.CharFilter(field_name='mine__name', lookup_expr='icontains', label='Mine')
    service = django_filters.ModelChoiceFilter(queryset=ProfService.objects.all(), label='Service Provider')
    status = django_filters.ChoiceFilter(choices=STATUS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Valid Until:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = FieldReq
        fields = ('__all__', 'date_range')

    def filter(self, period__gte, period__lte):
        pass


class FieldAttachFilter(django_filters.FilterSet):

    TYPE = (
        ('Technical', 'Technical'),
        ('Receipts', 'Receipts'),
    )

    id = django_filters.NumberFilter(label='Field Attach Ref')
    name = django_filters.CharFilter(lookup_expr='icontains', label='Attachment Name')
    type = django_filters.ChoiceFilter(choices=TYPE)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = FieldAttachments
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineviewArchiveLetterFilter(django_filters.FilterSet):

    MINELETTERS = (
        ('Mines Ministry', 'Mines Ministry'),
        ('Government', 'Government'),
        ('Other', 'Other'),
    )
    INOUT = (
        ('In', 'In'),
        ('Out', 'Out'),
    )

    mine = django_filters.CharFilter(field_name='mine__name', lookup_expr='icontains', label='Mine')
    other_party = django_filters.CharFilter(lookup_expr='icontains', label='Other Party')
    type = django_filters.ChoiceFilter(choices=MINELETTERS)
    inout = django_filters.ChoiceFilter(choices=INOUT, label='To / From')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineLetters
        fields = ('__all__', 'date_range')

    def filter(self, report_date__gte, report_date__lte):
        pass


class MineviewWorksFilter(django_filters.FilterSet):

    MINELETTERS = (
        ('Mines Ministry', 'Mines Ministry'),
        ('Government', 'Government'),
        ('Other', 'Other'),
    )
    INOUT = (
        ('In', 'In'),
        ('Out', 'Out'),
    )

    mine = django_filters.CharFilter(field_name='mine__name', lookup_expr='icontains', label='Mine')
    other_party = django_filters.CharFilter(lookup_expr='icontains', label='Other Party')
    type = django_filters.ChoiceFilter(choices=MINELETTERS)
    inout = django_filters.ChoiceFilter(choices=INOUT, label='To / From')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineLetters
        fields = ('__all__', 'date_range')

    def filter(self, report_date__gte, report_date__lte):
        pass


class MineviewArchiveAgreementFilter(django_filters.FilterSet):

    works = django_filters.CharFilter(field_name='works__works', lookup_expr='icontains', label='Description')
    comment = django_filters.CharFilter(lookup_expr='icontains', label='Comment')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineWorks
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineviewPlantFilter(django_filters.FilterSet):

    plant = django_filters.CharFilter(field_name='plant__plant', lookup_expr='icontains', label='Description')
    comment = django_filters.CharFilter(lookup_expr='icontains', label='Comment')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MinePlant
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineviewMobileFilter(django_filters.FilterSet):

    works = django_filters.CharFilter(field_name='plant__plant', lookup_expr='icontains', label='Description')
    comment = django_filters.CharFilter(lookup_expr='icontains', label='Comment')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date Created:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineYellowPlant
        fields = ('__all__', 'date_range')

    def filter(self, date_created__gte, date_created__lte):
        pass


class MineviewArchiveReceiptFilter(django_filters.FilterSet):
    MINERECEIPTS = (
        ('Inspection', 'Inspection'),
        ('Registration', 'Registration'),
        ('Site', 'Site'),
        ('Explosives', 'Explosives'),
        ('Fine', 'Fine'),
        ('Other', 'Other'),
    )

    mine = django_filters.CharFilter(field_name='mine__name', lookup_expr='icontains', label='Mine')
    rec_number = django_filters.NumberFilter(label='Receipt Number')
    type = django_filters.ChoiceFilter(choices=MINERECEIPTS)

    date_range = django_filters.DateFromToRangeFilter(
        label='Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = MineReceipts
        fields = ('__all__', 'date_range')

    def filter(self, report_date__gte, report_date__lte):
        pass


class MineviewArchiveOtherFilter(django_filters.FilterSet):

    TYPE = (
        ('Technical', 'Technical'),
        ('Receipts', 'Receipts'),
    )

    mine = django_filters.CharFilter(field_name='mine__name', lookup_expr='icontains', label='Mine')
    subject = django_filters.CharFilter(lookup_expr='icontains', label='Subject')

    date_range = django_filters.DateFromToRangeFilter(
        label='Date:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = OtherDocs
        fields = ('__all__', 'date_range')

    def filter(self, report_date__gte, report_date__lte):
        pass


class CartRequestFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(label='Cart Request Ref')
    mineral = django_filters.ModelChoiceFilter(queryset=Mineral.objects.all(), label='Mineral')
    # mineral = django_filters.CharFilter(field_name='mineral__name', lookup_expr='icontains', label='Mineral')
    invest_type = django_filters.ChoiceFilter(choices=INVESTYPE)

    date_range = django_filters.DateFromToRangeFilter(
        label='Valid Date Range:',
        method=filter_by_range,
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'})
    )

    class meta:
        model = CartRequest
        fields = ('__all__', 'date_range')

    def filter(self, valid__gte, valid__lte):
        pass