import django_filters
from django import forms
from django.db.models import Q
from .models import *
from django.forms import MultipleChoiceField, ChoiceField, Form, Select, widgets
from django.forms.widgets import NumberInput, CheckboxSelectMultiple
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
            'agents',
        ]

    def __init__(self, *args, **kwargs):
        super(IndividualForm, self).__init__(*args, **kwargs)
        agent_list =[]

        for user in User.objects.all():
            if CorpAgentRelation.objects.filter(agent_id=user.id).exists():
                pass
            else:
                if SyndAgentRelation.objects.filter(agent_id=user.id).exists():
                    pass
                else:
                    if IndiAgentRelation.objects.filter(agent_id=user.id).exists():
                        pass
                    else:
                        agent_list.append(user.id)

        self.fields['agents'].queryset = User.objects.filter(id__in=agent_list)


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

    def __init__(self, *args, **kwargs):
        super(CorporateForm, self).__init__(*args, **kwargs)
        agent_list =[]

        for user in User.objects.all():
            if CorpAgentRelation.objects.filter(agent_id=user.id).exists():
                pass
            else:
                if SyndAgentRelation.objects.filter(agent_id=user.id).exists():
                    pass
                else:
                    if IndiAgentRelation.objects.filter(agent_id=user.id).exists():
                        pass
                    else:
                        agent_list.append(user.id)

        self.fields['agents'].queryset = User.objects.filter(id__in=agent_list)


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

    def __init__(self, *args, **kwargs):
        super(SyndicateForm, self).__init__(*args, **kwargs)
        agent_list =[]

        for user in User.objects.all():
            if CorpAgentRelation.objects.filter(agent_id=user.id).exists():
                pass
            else:
                if SyndAgentRelation.objects.filter(agent_id=user.id).exists():
                    pass
                else:
                    if IndiAgentRelation.objects.filter(agent_id=user.id).exists():
                        pass
                    else:
                        agent_list.append(user.id)

        self.fields['agents'].queryset = User.objects.filter(id__in=agent_list)


class MandateForm(forms.ModelForm):
    valid = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(choices=MANDATESTATUS, label='Mandate Purpose')

    class Meta:
        model = Mandate
        fields = [
            'valid',
            'status',
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
            # 'phone_number',
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
            # 'phone_number',
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
        claims = MineClaimRelation.objects.all()
        claim_list = []
        for claim in claims:
            claim_list.append(claim.claim.id)

        self.fields['claim'].queryset = MiningClaim.objects.filter(~Q(id__in=claim_list))


class AttachReportForm(forms.ModelForm):
    report_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    pdf = forms.FileField()

    class Meta:
        model = MineReports
        fields = [
            'report_date',
            'type',
            'pdf',
        ]


class AttachLetterForm(forms.ModelForm):
    report_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label='Date')
    pdf = forms.FileField()

    class Meta:
        model = MineLetters
        fields = [
            'report_date',
            'type',
            'other_party',
            'subject',
            'mine',
            'pdf',
        ]

    def __init__(self, player=None, *args, **kwargs):
        super(AttachLetterForm, self).__init__(*args, **kwargs)
        owner_list = MineOwnerRelation.objects.filter(owner_id=player.id, status='Current')
        mine_list = []
        for owner in owner_list:
            mine_list.append(owner.mine.id)
        if player:
            self.fields['mine'].queryset = Mine.objects.filter(id__in=mine_list)


class AttachReceiptForm(forms.ModelForm):
    report_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    pdf = forms.FileField()

    class Meta:
        model = MineReceipts
        fields = [
            'report_date',
            'type',
            'issued_by',
            'rec_number',
            'mine',
            'pdf',
        ]

    def __init__(self, player=None, *args, **kwargs):
        super(AttachReceiptForm, self).__init__(*args, **kwargs)
        owner_list = MineOwnerRelation.objects.filter(owner_id=player.id, status='Current')
        mine_list = []
        for owner in owner_list:
            mine_list.append(owner.mine.id)
        if player:
            self.fields['mine'].queryset = Mine.objects.filter(id__in=mine_list)


class AttachAgreementForm(forms.ModelForm):
    report_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label='Date Signed')
    valid_to = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label='Valid Until')
    pdf = forms.FileField()
    addendum = forms.BooleanField()

    class Meta:
        model = MineAgreements
        fields = [
            'report_date',
            'valid_to',
            'type',
            'counter_party',
            'mine',
            'pdf',
        ]

    def __init__(self, player=None, *args, **kwargs):
        super(AttachAgreementForm, self).__init__(*args, **kwargs)
        owner_list = MineOwnerRelation.objects.filter(owner_id=player.id, status='Current')
        mine_list = []
        for owner in owner_list:
            mine_list.append(owner.mine.id)
        if player:
            self.fields['mine'].queryset = Mine.objects.filter(id__in=mine_list)


class AttachOtherDocForm(forms.ModelForm):
    report_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    pdf = forms.FileField()

    class Meta:
        model = OtherDocs
        fields = [
            'report_date',
            'subject',
            'mine',
            'pdf',
        ]

    def __init__(self, player=None, *args, **kwargs):
        super(AttachOtherDocForm, self).__init__(*args, **kwargs)
        owner_list = MineOwnerRelation.objects.filter(owner_id=player.id, status='Current')
        mine_list = []
        for owner in owner_list:
            mine_list.append(owner.mine.id)
        if player:
            self.fields['mine'].queryset = Mine.objects.filter(id__in=mine_list)


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
            'type',
            'pdf',
        ]


class AttachClaimCertForm(forms.ModelForm):
    pdf = forms.ImageField()

    class Meta:
        model = ClaimRegCert
        fields = [
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


class AssayForm(forms.ModelForm):
    sample_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Assays
        fields = [
            'sample_date',
            'mineral',
            'assay',
            'unit',
        ]


class SamplePointForm(forms.ModelForm):
    sample_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    mineral = forms.ModelChoiceField(Elements.objects.all())
    assay = forms.FloatField()
    unit = forms.ModelChoiceField(AssayUnits.objects.all())

    class Meta:
        model = SamplePoint
        fields = [
            'name',
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
            'mine',
            'plant',
            'quantity',
            'serial_number',
            'comment',
        ]

    def __init__(self, player=None, *args, **kwargs):
        super(MinePlantForm, self).__init__(*args, **kwargs)
        owner_list = MineOwnerRelation.objects.filter(owner_id=player.id, status='Current')
        mine_list = []
        for owner in owner_list:
            mine_list.append(owner.mine.id)
        if player:
            self.fields['mine'].queryset = Mine.objects.filter(id__in=mine_list)


class MineYellowPlantForm(forms.ModelForm):
    when_new = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = MineYellowPlant
        fields = [
            'plant',
            'model',
            'when_new',
            'quantity',
            'serial_number',
            'comment',
        ]


class PlantImageForm(forms.ModelForm):
    plant = forms.ImageField()

    class Meta:
        model = PlantImages
        fields = [
            'plant',
        ]


class PlantServiceForm(forms.ModelForm):
    service_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    next_service = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = EquipmentService
        fields = [
            'service_date',
            'next_service',
            'comment',
        ]


class WorksDevForm(forms.ModelForm):
    dev_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = WorksDev
        fields = [
            'dev_date',
            'comment',
        ]


class PlantUsageForm(forms.ModelForm):
    reading_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = EquipmentMileage
        fields = [
            'reading_date',
            'mileage',
            'usage_time',
        ]


class YellowImageForm(forms.ModelForm):
    plant = forms.ImageField()

    class Meta:
        model = YellowImages
        fields = [
            'plant',
        ]


class WorksImageForm(forms.ModelForm):
    plant = forms.ImageField()

    class Meta:
        model = WorksImages
        fields = [
            'plant',
        ]


class MineWorksForm(forms.ModelForm):

    class Meta:
        model = MineWorks
        fields = [
            'mine',
            'works',
            'quantity',
            'comment',
        ]

    def __init__(self, player=None, *args, **kwargs):
        super(MineWorksForm, self).__init__(*args, **kwargs)
        owner_list = MineOwnerRelation.objects.filter(owner_id=player.id, status='Current')
        mine_list = []
        for owner in owner_list:
            mine_list.append(owner.mine.id)
        if player:
            self.fields['mine'].queryset = Mine.objects.filter(id__in=mine_list)


class MandateRequestForm(forms.ModelForm):
    duration = forms.IntegerField(label='Duration in Days')
    period = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label='Inception Date')

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
            'country',
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
