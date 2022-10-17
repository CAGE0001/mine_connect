import django_filters
from django import forms
from .models import *
from django.forms import MultipleChoiceField, ChoiceField, Form, Select, widgets
from django.forms.widgets import NumberInput
from datetime import timedelta, timezone, date
from leaflet.forms.widgets import LeafletWidget
from leaflet.forms.fields import PolygonField

OWNERSTATUS = (
    ('Current', 'Current'),
    ('Tributed', 'Tributed'),
    ('Sold', 'Sold'),
    ('Forfeited', 'Forfeited')
)


MANDATESTATUS = (
    ('Free', 'Free'),
    ('Desktop', 'Desktop'),
    ('Field', 'Field'),
    ('Exclusive Option', 'Exclusive Option'),
    ('Negotiation', 'Negotiation'),
    ('Success', 'Success'),
)


class IndividualForm(forms.ModelForm):
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = IndRecord
        fields = [
            'first_name',
            'last_name',
            'sex',
            'dob',
            'nationality',
            'nid',
        ]


class IndiStatUpdate(forms.ModelForm):
    class Meta:
        model = IndRecord
        fields = [
        ]


class SyndStatUpdate(forms.ModelForm):
    class Meta:
        model = Syndicate
        fields = [
        ]


class CorpStatUpdate(forms.ModelForm):
    class Meta:
        model = CorpRecord
        fields = [
        ]


class IndividualEditForm(forms.ModelForm):
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = IndRecord
        fields = [
            'first_name',
            'last_name',
            'sex',
            'dob',
            'nationality',
            'nid',
        ]


class CorporateForm(forms.ModelForm):
    doi = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = CorpRecord
        fields = [
            'name',
            'type',
            'doi',
            'nationality',
            'reg_number',
            'agents'
        ]


class WorkHistoryForm(forms.ModelForm):
    from_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = SerProvProfile
        fields = [
            'principal',
            'title',
            'from_date',
            'to_date',
            'description',
            'reference',
            'ref_contact',
            'role',
        ]


class CorporateEditForm(forms.ModelForm):
    doi = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = CorpRecord
        fields = [
            'name',
            'type',
            'doi',
            'nationality',
            'reg_number',
            'agents',
        ]


class GetQuoteForm(forms.ModelForm):

    class Meta:
        model = FieldActivityQoutes
        fields = [
        ]


class FieldStatusForm(forms.ModelForm):

    class Meta:
        model = Field
        fields = [
        ]


class CartMatchForm(forms.ModelForm):
    valid = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = CartMineMatch
        fields = [
            'mines',
            'valid',
        ]


class InvestorMineForm(forms.ModelForm):

    class Meta:
        model = InvestorMineRelation
        fields = [
        ]


class ClaimStatusForm(forms.ModelForm):

    class Meta:
        model = MiningClaim
        fields = [
        ]


class PlayerTrxnForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = [
        ]


class CashInForm(forms.ModelForm):

    class Meta:
        model = PlayerCash
        fields = [
            'amount',
            'ref',
        ]


class SyndicateForm(forms.ModelForm):
    dor = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Syndicate
        fields = [
            'name',
            'dor',
            'members',
            'agents',
        ]


class MandateForm(forms.ModelForm):
    valid = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Mandate
        fields = [
            'valid',
            'mine',
        ]


class FieldReqForm(forms.ModelForm):
    period = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    pdf = forms.FileField()

    class Meta:
        model = FieldReq
        fields = [
            'service',
            'period',
            'description',
            'pdf'
        ]


class SubmitQuoteForm(forms.ModelForm):

    class Meta:
        model = FieldProviderQuote
        fields = [
            'cost',
            'comment',
        ]


class SupportCostForm(forms.ModelForm):

    class Meta:
        model = FieldSupCosts
        fields = [
            'cost_type',
            'cost',
            'comment',
        ]


class QuoteAcceptForm(forms.ModelForm):

    class Meta:
        model = FieldReqWinQte
        fields = [

        ]


class FieldReqCounterForm(forms.ModelForm):

    class Meta:
        model = FieldProviderQuote
        fields = [
            'counter_offer',
        ]


class FieldReqWinQteForm(forms.ModelForm):

    class Meta:
        model = FieldReqWinQte
        fields = [
        ]


class FieldServStatForm(forms.ModelForm):

    class Meta:
        model = ServiceProvRequired
        fields = [
        ]


class FieldProviderQuoteCounterForm(forms.ModelForm):

    class Meta:
        model = FieldProviderQuote
        fields = [
        ]


class FieldProformaForm(forms.ModelForm):

    class Meta:
        model = FieldProforma
        fields = [
            'admin_premium',
        ]


class FieldInvestorForm(forms.ModelForm):

    class Meta:
        model = FieldProforma
        fields = [
            'admin_premium',
        ]


class FieldForm(forms.ModelForm):

    from_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Field
        fields = [
            'subject',
            'task',
            'from_date',
            'to_date',
            'provider',
            'mine_owner_requirements',
        ]

    # def __init__(self, providers, *args, **kwargs):
    #     super(FieldForm, self).__init__(*args, **kwargs)
    #     self.fields['provider'].queryset = ServiceProv.objects.filter(mine_attach='None')


class RequestProviderForm(forms.ModelForm):
    quantity = forms.IntegerField()

    class Meta:
        model = FieldReq
        fields = [
            'provider_roles',
            'quantity',
        ]


class SPReqForm(forms.ModelForm):
    quantity = forms.IntegerField()

    class Meta:
        model = ServiceProvRequired
        fields = [
        ]


class FieldReqStatForm(forms.ModelForm):

    class Meta:
        model = FieldReq
        fields = [
        ]


class ProformaStatusForm(forms.ModelForm):

    class Meta:
        model = FieldProforma
        fields = [
        ]


class SyndicateEditForm(forms.ModelForm):
    dor = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Syndicate
        fields = [
            'name',
            'dor',
            'members',
            'agents',
        ]


class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = [
            # 'name',
            'phone_number',
            'email',
            'bank',
            'bank_account',
            'street_address',
            'suburb',
            'city',
            'country',
            'trxn_balance',
        ]


class PlayerEditForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = [
            # 'name',
            'phone_number',
            'email',
            'bank',
            'bank_account',
            'street_address',
            'suburb',
            'city',
            'country',
            'trxn_balance',
        ]


class MineInvestReqForm(forms.ModelForm):
    valid = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = MineInvestReq
        fields = [
            'invest_type',
            'valid',
            'value',
            'conglomerate',
        ]


class NewMineForm(forms.ModelForm):
    insp_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Mine
        fields = [
            'name',
            'mineral',
            'insp_date',
            'resource_type',
            'reserves_proven',
            'reserves_possible',
            'reserves_probable',
            'insp_status',
            'country',
        ]


class NewClaimForm(forms.ModelForm):
    reg_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = MiningClaim
        fields = [
            'reg_date',
            'name',
            'type',
            'reg_number',
            'area',
        ]


class MineClaimForm(forms.ModelForm):

    class Meta:
        model = MineClaimRelation
        fields = [
            'claim',
        ]

    def __init__(self, *args, **kwargs):
        super(MineClaimForm, self).__init__(*args, **kwargs)
        self.fields['claim'].queryset = MiningClaim.objects.filter(mine_attach='None')


class AttachReportForm(forms.ModelForm):
    report_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    pdf = forms.FileField()

    class Meta:
        model = MineReports
        fields = [
            'report_date',
            'mine',
            'type',
            'pdf',
        ]


class FieldAttachForm(forms.ModelForm):
    pdf = forms.FileField()

    class Meta:
        model = FieldAttachments
        fields = [
            'type',
            'name',
        ]


class FieldAcquitForm(forms.ModelForm):

    class Meta:
        model = FieldAcquit
        fields = [
            'comment',
            'recommendation',
        ]


class AttachCertForm(forms.ModelForm):
    issue_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    pdf = forms.ImageField()

    class Meta:
        model = MineCertificates
        fields = [
            'issue_date',
            'mine',
            'type',
            'pdf',
        ]


class AttachClaimCertForm(forms.ModelForm):
    issue_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    pdf = forms.ImageField()

    class Meta:
        model = ClaimRegCert
        fields = [
            'issue_date',
            'claim',
            'pdf',
        ]


class AttachToMineForm(forms.ModelForm):

    class Meta:
        model = MineClaimRelation
        fields = [
            'mine',
        ]


class DummyForm(forms.ModelForm):

    class Meta:
        model = Dummy
        fields = [
            'location',
        ]


class BeaconPolyForm(forms.ModelForm):

    class Meta:
        model = MiningClaimPolygon
        fields = [
        ]


class ClaimLocForm(forms.ModelForm):

    class Meta:
        model = MiningClaimLocation
        fields = [
        ]


class BeaconForm(forms.ModelForm):

    class Meta:
        model = Beacon
        fields = [
            'latitude',
            'longitude',
        ]


class ClaimEditForm(forms.ModelForm):
    reg_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = MiningClaim
        fields = [
            'reg_date',
            'name',
            'type',
            'reg_number',
        ]


class MineEditForm(forms.ModelForm):
    insp_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Mine
        fields = [
            'name',
            'mineral',
            'insp_date',
            'resource_type',
            'reserves_proven',
            'reserves_possible',
            'reserves_probable',
            'insp_status',
            'claim',
        ]

    def __init__(self, *args, **kwargs):
        super(MineEditForm, self).__init__(*args, **kwargs)
        self.fields['claim'].queryset = MiningClaim.objects.filter(mine_attach='None')


class MineEmployeeForm(forms.ModelForm):
    insp_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    pdf = forms.FileField()

    class Meta:
        model = MineEmployees
        fields = [
            'employee',
            'job',
            'post',
            'pdf',
        ]


class MineOwnerForm(forms.ModelForm):

    class Meta:
        model = MineOwnerRelation
        fields = [
            'mine',
        ]


class InvestorForm(forms.ModelForm):

    class Meta:
        model = Investor
        fields = [
        ]


class CartMineForm(forms.ModelForm):
    valid = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = CartMineMatch
        fields = [
            'mines',
            'valid',
        ]


class MineProductionForm(forms.ModelForm):
    start_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = MineProduction
        fields = [
            'material',
            'mineral',
            'start_date',
            'end_date',
            'quantity',
            'unit',
        ]


class MineLabourForm(forms.ModelForm):

    class Meta:
        model = MineLabour
        fields = [
            'management',
            'skilled',
            'semi_skilled',
            'unskilled',
        ]


class MinePlantForm(forms.ModelForm):

    class Meta:
        model = MinePlant
        fields = [
            'plant',
            'quantity',
            'comment',
        ]


class MineYellowPlantForm(forms.ModelForm):

    class Meta:
        model = MineYellowPlant
        fields = [
            'plant',
            'quantity',
            'comment',
        ]


class MineWorksForm(forms.ModelForm):

    class Meta:
        model = MineWorks
        fields = [
            'works',
            'quantity',
            'comment',
        ]


class MandateRequestForm(forms.ModelForm):
    period = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = MandateRequest
        fields = [
            'purpose',
            'duration',
            'period',
        ]

    # def __init__(self, cart_mine_match, *args, **kwargs):
    #     super(MandateRequestForm, self).__init__(*args, **kwargs)
    #     self.fields['mines'].queryset = CartMineRelation.objects.filter(cart=cart_mine_match)


class MandateProformaForm(forms.ModelForm):

    class Meta:
        model = MandateProforma
        fields = [
            'amount',
        ]

    # def __init__(self, cart_mine_match, *args, **kwargs):
    #     super(MandateRequestForm, self).__init__(*args, **kwargs)
    #     self.fields['mines'].queryset = CartMineRelation.objects.filter(cart=cart_mine_match)


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = [
            'purpose',
        ]

    # def __init__(self, cart_mine_match, *args, **kwargs):
    #     super(MandateRequestForm, self).__init__(*args, **kwargs)
    #     self.fields['mines'].queryset = CartMineRelation.objects.filter(cart=cart_mine_match)


class InvoiceTrxnForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = [
        ]

    # def __init__(self, cart_mine_match, *args, **kwargs):
    #     super(MandateRequestForm, self).__init__(*args, **kwargs)
    #     self.fields['mines'].queryset = CartMineRelation.objects.filter(cart=cart_mine_match)


class TrxnForm(forms.ModelForm):

    class Meta:
        model = Trxns
        fields = [
        ]

    # def __init__(self, cart_mine_match, *args, **kwargs):
    #     super(MandateRequestForm, self).__init__(*args, **kwargs)
    #     self.fields['mines'].queryset = CartMineRelation.objects.filter(cart=cart_mine_match)


class TrxnMandateProForm(forms.ModelForm):

    class Meta:
        model = MandateProforma
        fields = [
        ]

    # def __init__(self, cart_mine_match, *args, **kwargs):
    #     super(MandateRequestForm, self).__init__(*args, **kwargs)
    #     self.fields['mines'].queryset = CartMineRelation.objects.filter(cart=cart_mine_match)


class AlertEditForm(forms.ModelForm):

    class Meta:
        model = Alerts
        fields = [
        ]


class CartRequestForm(forms.ModelForm):
    valid = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = CartRequest
        fields = [
            'valid',
            'mineral',
            'deposit_type',
            'resource_unit',
            'min_grade',
            'grade_unit',
            'invest_type',
            'location',
            'polygon',
        ]
        widgets = {'polygon': LeafletWidget(attrs={'loadevent': ''})}


class ServiceProvForm(forms.ModelForm):

    class Meta:
        model = ServiceProv
        fields = [
            'service',
            'rating',
        ]


class MineEmployeeEditForm(forms.ModelForm):
    insp_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    # pdf = forms.FileField()

    class Meta:
        model = MineEmployees
        fields = [
            'job',
            'post',
            # 'pdf',
        ]
