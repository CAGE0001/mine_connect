from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import *


class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'nationality')


admin.site.register(Country, CountryAdmin)


class MineLabourAdmin(admin.ModelAdmin):
    list_display = ('mine', 'staff')


admin.site.register(MineLabour, MineLabourAdmin)


class FieldAcquitAdmin(admin.ModelAdmin):
    list_display = ('activity', 'acquit')


admin.site.register(FieldAcquit, FieldAcquitAdmin)


class MineWorksAdmin(LeafletGeoAdmin):
    list_display = ('mine', 'works')


admin.site.register(MineWorks, MineWorksAdmin)


class MinePlantAdmin(admin.ModelAdmin):
    list_display = ('mine', 'plant')


admin.site.register(MinePlant, MinePlantAdmin)


class MineYellowPlantAdmin(admin.ModelAdmin):
    list_display = ('mine', 'plant')


admin.site.register(MineYellowPlant, MineYellowPlantAdmin)


class MineProductionAdmin(admin.ModelAdmin):
    list_display = ('mine', 'material', 'mineral', 'quantity')


admin.site.register(MineProduction, MineProductionAdmin)


class IndRecordAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


admin.site.register(IndRecord, IndRecordAdmin)


class CorpRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


admin.site.register(CorpRecord, CorpRecordAdmin)


class SyndicateAdmin(admin.ModelAdmin):
    list_display = ('name', 'dor')


admin.site.register(Syndicate, SyndicateAdmin)


class InvestorMineRelationAdmin(admin.ModelAdmin):
    list_display = ('investor', 'mine')


admin.site.register(InvestorMineRelation, InvestorMineRelationAdmin)
admin.site.register(Beacon)
admin.site.register(TemplateLinks)
admin.site.register(ServerIP)
admin.site.register(MandateTypeList)
admin.site.register(PlayerUserRelation)
admin.site.register(SyndMemberRelation)
admin.site.register(YellowList)
admin.site.register(PlantList)
admin.site.register(WorksList)
admin.site.register(CorpAgentRelation)
admin.site.register(SyndAgentRelation)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


admin.site.register(Player, PlayerAdmin)


class PlayerCertificatesAdmin(admin.ModelAdmin):
    list_display = ('player', 'type', 'issue_date')


admin.site.register(PlayerCertificates, PlayerCertificatesAdmin)
admin.site.register(Mineral)
admin.site.register(DepositType)


class MiningClaimAdmin(LeafletGeoAdmin):
    list_display = ('name', 'type', 'reg_date')


admin.site.register(MiningClaim, MiningClaimAdmin)


class MiningClaimLocationAdmin(LeafletGeoAdmin):
    list_display = ('name', 'location')


admin.site.register(MiningClaimLocation, MiningClaimLocationAdmin)


class MiningClaimBeaconsAdmin(LeafletGeoAdmin):
    list_display = ('name', 'location')


admin.site.register(MiningClaimBeacons, MiningClaimBeaconsAdmin)


class MiningClaimPolygonAdmin(LeafletGeoAdmin):
    list_display = ('name', 'location')


admin.site.register(MiningClaimPolygon, MiningClaimPolygonAdmin)


class MineInvestReqAdmin(admin.ModelAdmin):
    list_display = ('mine', 'invest_type', 'value')


admin.site.register(MineInvestReq, MineInvestReqAdmin)


class MineAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource_type')


admin.site.register(Mine, MineAdmin)


class MineLocationAdmin(LeafletGeoAdmin):
    list_display = ('name', 'location')


admin.site.register(MineLocation, MineLocationAdmin)


class MinePolygonAdmin(LeafletGeoAdmin):
    list_display = ('name', 'polygon')


admin.site.register(MinePolygon, MinePolygonAdmin)


class MandateProformaAdmin(admin.ModelAdmin):
    list_display = ('mandate_request', 'amount', 'status')


admin.site.register(MandateProforma, MandateProformaAdmin)
admin.site.register(MineOwnerRelation)
admin.site.register(MineClaimRelation)
admin.site.register(MineMineral)
admin.site.register(MineJobList)
admin.site.register(FiedlProviderRelation)
admin.site.register(FiedlMineRequirements)


class MineEmployeesAdmin(admin.ModelAdmin):
    list_display = ('employee', 'job', 'post')


admin.site.register(MineEmployees, MineEmployeesAdmin)


class MineCertificatesAdmin(admin.ModelAdmin):
    list_display = ('mine', 'type', 'issue_date')


admin.site.register(MineCertificates, MineCertificatesAdmin)


class MineReportsAdmin(admin.ModelAdmin):
    list_display = ('mine', 'type', 'report_date')


admin.site.register(MineReports, MineReportsAdmin)


class ClaimRegCertAdmin(admin.ModelAdmin):
    list_display = ('claim', 'issue_date')


admin.site.register(ClaimRegCert, ClaimRegCertAdmin)
# admin.site.register(Beacon)


class InvestorAdmin(admin.ModelAdmin):
    list_display = ('player', 'date_created')


admin.site.register(Investor, InvestorAdmin)


class CartRequestAdmin(admin.ModelAdmin):
    list_display = ('investor', 'mineral', 'invest_type')


admin.site.register(CartRequest, CartRequestAdmin)


class CartMineMatchAdmin(admin.ModelAdmin):
    list_display = ('cart_request', 'valid')


admin.site.register(CartMineMatch, CartMineMatchAdmin)
admin.site.register(CartMineRelation)


class MandateRequestAdmin(admin.ModelAdmin):
    list_display = ('cart_mine_match', 'period')


admin.site.register(MandateRequest, MandateRequestAdmin)
admin.site.register(MineMandateRequest)


class MandateAdmin(admin.ModelAdmin):
    list_display = ('mandate_request', 'valid')


admin.site.register(Mandate, MandateAdmin)
admin.site.register(MineMandateRelation)


class ProfServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created')


admin.site.register(ProfService, ProfServiceAdmin)


class FieldReqAdmin(admin.ModelAdmin):
    list_display = ('status', 'mandate')


admin.site.register(FieldReq, FieldReqAdmin)


class ServiceProvRequiredAdmin(admin.ModelAdmin):
    list_display = ('field_request', 'provider_role')


admin.site.register(ServiceProvRequired, ServiceProvRequiredAdmin)


class AffiliationsAdmin(admin.ModelAdmin):
    list_display = ('player', 'organisation')



admin.site.register(Affiliations, AffiliationsAdmin)


class FieldProviderQuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_ref', 'provider')



admin.site.register(FieldProviderQuote, FieldProviderQuoteAdmin)


class FieldSupCostsAdmin(admin.ModelAdmin):
    list_display = ('field_request', 'cost_type')



admin.site.register(FieldSupCosts, FieldSupCostsAdmin)


class FieldReqWinQteAdmin(admin.ModelAdmin):
    list_display = ('service_ref', 'quote')



admin.site.register(FieldReqWinQte, FieldReqWinQteAdmin)
admin.site.register(AdminPremium)
admin.site.register(FieldCostList)
admin.site.register(AffiliateOrgs)
admin.site.register(FieldProforma)
admin.site.register(ServiceProvRole)


class ServiceProvAdmin(admin.ModelAdmin):
    list_display = ('name', 'service')


admin.site.register(ServiceProv, ServiceProvAdmin)


class SerProvProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')


admin.site.register(SerProvProfile, SerProvProfileAdmin)


class FieldAdmin(admin.ModelAdmin):
    list_display = ('proforma', 'from_date')


admin.site.register(Field, FieldAdmin)
admin.site.register(TrxnPurpose)


class TrxnsAdmin(admin.ModelAdmin):
    list_display = ('payer', 'amount', 'purpose')


admin.site.register(Trxns, TrxnsAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('payer', 'amount', 'purpose')


admin.site.register(Invoice, InvoiceAdmin)


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'trxn_ref', 'amount')


admin.site.register(Receipt, ReceiptAdmin)


class FieldInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'field_proforma')


admin.site.register(FieldInvoice, FieldInvoiceAdmin)


class FieldActivityQoutesAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'activity', 'status')


admin.site.register(FieldActivityQoutes, FieldActivityQoutesAdmin)


class FieldAttachmentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'activity')


admin.site.register(FieldAttachments, FieldAttachmentsAdmin)
#
#
# class BeaconAdmin(admin.ModelAdmin):
#     list_display = ('symbol', 'location')
#
#
# admin.site.register(Beacon, BeaconAdmin)
