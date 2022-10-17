from django.urls import path, include
from .import views

urlpatterns = [
    path('index', views.index, name='index.html'),
    path('owner_index', views.owner_index, name='mine_owner/owner_index.html'),
    path('investor_index', views.investor_index, name='investor/investor_index.html'),
    path('provider_index', views.provider_index, name='services/provider_index.html'),
    path('', views.login, name='login.html'),
    path('login', views.login, name='login.html'),
    path('logout', views.logout, name='logout'),
    path('confirm_logout', views.confirm_logout, name='confirm_logout.html'),
    path('owner_type', views.owner_type, name='owner_type.html'),
    path('module_options', views.module_options, name='module_options.html'),

    path('cart_request/<str:pk>/create/', views.create_cart_request, name='investor/cart_request_create.html'),
    path('cart_request/<str:pk>/detail/', views.cart_request_detail, {'template': 'investor/cart_request_detail.html'}, name='investor/cart_request_detail.html'),
    path('cart_request/<str:pk>/mandate/', views.cart_request_detail, {'template': 'investor/cart_req_mandate.html'}, name='investor/cart_req_mandate.html'),
    path('cart_request/<str:pk>/field_request/', views.cart_request_detail, {'template': 'investor/cart_field_request.html'}, name='investor/cart_field_request.html'),
    path('cart_request/<str:pk>/field_activity/', views.cart_request_detail, {'template': 'investor/cart_field_activity.html'}, name='investor/cart_field_activity.html'),
    path('cart_request_list/', views.cart_request_list, name='investor/cart_request_list.html'),

    path('cart_mine_match/<str:pk>/create/', views.create_cart_mine_match, name='investor/create_cart_mine_match.html'),
    path('cart_mine_match/<str:pk>/edit/', views.edit_cart_mine_match, name='investor/edit_cart_mine_match.html'),
    path('cart_mine_match/lists/', views.cart_mine_match_list, name='investor/cart_mine_match_list.html'),

    path('player/<str:pk>/detail/', views.player_detail, name='player_detail.html'),
    path('player/<str:pk>/mine/detail/', views.player_detail_mine, name='player_detail_mines.html'),
    path('player/<str:pk>/<str:template_name>/detail_general/', views.player_detail_investor, name='player_detail_investor.html'),
    path('player/<str:pk>/investor/detail/', views.player_detail_investor, name='player_detail_investor.html'),
    path('player/<str:pk>/service/detail/', views.player_detail_service, name='player_detail_services.html'),
    path('player/<str:pk>/receipts/detail/', views.player_detail_receipts, name='player_detail_receipts.html'),
    path('player/<str:pk>/payments/detail/', views.player_detail_payments, name='player_detail_payments.html'),
    path('player_list/', views.player_list, name='player_list.html'),
    path('player_individual/lists/', views.player_individuals_list, name='individuals_list.html'),
    path('player_syndicate/lists/', views.player_syndicate_list, name='syndicate_list.html'),
    path('player_company/lists/', views.player_company_list, name='company_list.html'),

    path('mandate_request/<str:pk>/create/', views.create_mandate_request, name='investor/mandate_request_create.html'),
    path('mandate_request/<str:pk>/detail/', views.investor_mandate_request_detail, name='investor/mandate_request_detail.html'),
    path('mandate_request/<str:pk>/field_req_detail/', views.investor_mandate_request_field_req_detail, name='investor/mandate_request_field_req.html'),
    path('mandate_request/<str:pk>/field_act_detail/', views.investor_mandate_request_field_act_detail, name='investor/mandate_request_field_act.html'),
    path('mandate_request_list/', views.mandate_request_list, name='investor/mandate_request_list.html'),

    path('work_history/<str:pk>/create/', views.create_work_history, name='services/work_history.html'),

    path('mandate/<str:pk>/detail/', views.investor_mandate_detail, name='investor/mandate_detail.html'),
    path('mandate/<str:pk>/detail/field_act', views.mandate_detail_field_activity, name='investor/mandate_detail_field_activity.html'),
    path('mandate_list/', views.mandate_list, name='investor/mandate_list.html'),
    path('mandate/<str:pk>/create/', views.create_mandate, name='investor/mandate_create.html'),

    path('service/<str:pk>/detail/', views.service_detail, name='services/mandate_detail.html'),
    path('service/<str:pk>/detail/', views.service_detail_activity, name='services/detail_activities.html'),

    path('claim_reg_cert/<str:pk>/detail/', views.claim_reg_cert_detail, name='claim_reg_cert_detail.html'),
    path('minewiew/claim_reg_cert/<str:pk>/detail/', views.mineview_claim_reg_cert_detail, name='mine_owner/claim_reg_cert_detail.html'),
    path('claim_reg_cert_list/', views.claim_reg_cert_list, name='claim_reg_cert_list.html'),
    path('claim_reg_cert_add/<str:pk>/', views.claim_reg_cert_add, name='claim_reg_cert_add.html'),

    path('investorview/cart/<str:pk>/mandate_requests/', views.investview_cart_detail, {'template': 'investor/investview/cart/mandate_request.html'}, name='investor/investview/cart/mandate_request.html'),
    path('investorview/cart/<str:pk>/mandates/', views.investview_cart_detail, {'template': 'investor/investview/cart/mandates.html'}, name='investor/investview/cart/mandates.html'),
    path('investorview/cart/<str:pk>/field_requests/', views.investview_cart_detail, {'template': 'investor/investview/cart/services.html'}, name='investor/investview/cart/services.html'),
    path('investorview/<str:pk>/cart_match/', views.investview_cart_match, name='investor/investview_cart_match.html'),
    path('investorview/<str:pk>/<str:pk1>/request_mandates/', views.investview_request_mandates, name='investor/investview_request_mandates.html'),
    path('investorview/cart/<str:pk>/field_activity/', views.investview_cart_detail, {'template': 'investor/investview/cart/field_activity.html'}, name='investor/investview/cart/field_activity.html'),
    path('investorview/cart/lists/', views.investview_cart_request_list, name='investor/investview/cart/list.html'),
    path('investorview/cart/<str:pk>/request/new/', views.investview_cart_request_new, name='investor/investview/cart/request.html'),

    path('investorview/mine/<str:pk>/claims/', views.mine_detail, {'template': 'investor/investview/mine/claims.html'}, name='investor/investview/mine/claims.html'),
    path('investorview/mine/<str:pk>/reports/', views.mine_detail, {'template': 'investor/investview/mine/reports.html'}, name='investor/investview/mine/reports.html'),
    path('investorview/mine/<str:pk>/map/', views.mine_detail, {'template': 'investor/mine_map.html'}, name='investor/mine_map.html'),

    path('provider/mine/<str:pk>/claims/', views.proview_mine_detail, {'template': 'services/proview/mine/claims.html'}, name='services/proview/mine/claims.html'),
    path('provider/mine/<str:pk>/reports/', views.proview_mine_detail, {'template': 'services/proview/mine/reports.html'}, name='services/proview/mine/reports.html'),
    path('provider/mine/<str:pk>/map/', views.proview_mine_detail, {'template': 'services/mine_map.html'}, name='services/mine_map.html'),

    path('investorview/mandate_request/<str:pk>/field_activity/', views.investview_mandate_request_field_act, name='investor/investview/mandate_request/field_activity.html'),
    path('investorview/mandate_request/<str:pk>/field_quote/', views.investview_mandate_request_field_quote, name='investor/investview/mandate_request/field_quote.html'),
    path('investorview/mandate_request/<str:pk>/field_request/', views.investview_mandate_request_field_req, name='investor/investview/mandate_request/services.html'),

    path('investorview/<str:pk>/invoice_detail/', views.investview_mandate_invoice_detail, name='investor/investview/mandate/invoice_detail.html'),
    path('investorview/mandate/<str:pk>/mandates/', views.investview_mandate_field_quote, name='investor/investview/mandate/field_quote.html'),
    path('investorview/mandate/<str:pk>/field_requests/', views.investview_mandate_field_act, name='investor/investview/mandate/field_activity.html'),
    path('investorview/mandate/<str:pk>/field_activity/', views.investview_mandate_field_req, name='investor/investview/mandate/services.html'),
    path('investorview/mandate/lists/', views.investview_mandate_list, name='investor/investview/mandate/list.html'),

    path('investorview/fieldreq/<str:pk>/quotes/', views.investview_field_req_quote_detail, name='investor/investview/fieldreq/field_quote.html'),
    path('investorview/fieldreq/<str:pk>/field_acts/', views.investview_field_req_act_detail, name='investor/investview/fieldreq/field_activity.html'),
    path('field_request/<str:pk>/create/', views.create_field_request, name='investor/field_request_create.html'),
    path('investorview/fieldreq/lists/', views.investview_field_request_list, name='investor/investview/fieldreq/list.html'),

    path('investorview/field/<str:pk>/attachments/', views.investview_field_detail, name='investor/investview/field/attach.html'),

    path('mineview_mines_list/', views.mine_view_list, name='mine_owner/mineview/lists.html'),
    path('investor_cart_list/', views.investview_cart_request_list, name='investor/investview/cart/lists.html'),

    path('mine_works/<str:pk>/add/', views.mine_works, name='mine_works.html'),
    path('mine_labour/<str:pk>/add/', views.mine_labour, name='mine_labour.html'),
    path('mine_plant/<str:pk>/add/', views.mine_plant, name='mine_plant.html'),
    path('mine_yellow_plant/<str:pk>/add/', views.mine_yellow_plant, name='mine_yellow_plant.html'),
    path('mine_production/<str:pk>/add/', views.mine_production, name='mine_production.html'),
    path('more_production_reports/<str:pk>/', views.more_production_reports, {'template': 'more_production_reports.html'}, name='more_production_reports.html'),
    path('more_production_reports_ore/<str:pk>/', views.more_production_reports, {'template': 'more_production_reports_ore.html'}, name='more_production_reports_ore.html'),
    path('more_production_reports_waste/<str:pk>/', views.more_production_reports, {'template': 'more_production_reports_waste.html'}, name='more_production_reports_waste.html'),
    path('plant_list/<str:pk>/', views.more_production_reports, {'template': 'plant_list.html'}, name='plant_list.html'),
    path('mine_works_list/<str:pk>/', views.more_production_reports, {'template': 'mine_works_list.html'}, name='mine_works_list.html'),
    path('yellow_plant_list/<str:pk>/', views.more_production_reports, {'template': 'yellow_plant_list.html'}, name='yellow_plant_list.html'),
    path('mineview_production_reports_mineral/<str:pk>/', views.more_production_reports, {'template': 'mineview_production_mineral.html'}, name='mineview_production_mineral.html'),
    path('mineview_production_reports_ore/<str:pk>/', views.more_production_reports, {'template': 'mineview_production_ore.html'}, name='mineview_production_ore.html'),
    path('mineview_production_reports_waste/<str:pk>/', views.more_production_reports, {'template': 'mineview_production_waste.html'}, name='mineview_production_waste.html'),
    path('mineview_mine_works/<str:pk>/', views.more_production_reports, {'template': 'mine_owner/mineview_mine_works.html'}, name='mineview_mine_works.html'),
    path('mineview_plant_and_equipment/<str:pk>/', views.more_production_reports, {'template': 'mine_owner/mineview_plant_list.html'}, name='mineview_plant_list.html'),
    path('mineview_mobile_plant/<str:pk>/', views.more_production_reports, {'template': 'mine_owner/mineview_yellow_plant.html'}, name='mineview_yellow_plant.html'),
    path('attach_to_mine/<str:pk>/', views.attach_to_mine, name='attach_to_mine.html'),

    path('beacon/<str:pk>/add/', views.add_beacon, name='add_beacon.html'),
    path('claim_boundary/<str:pk>/add/', views.claim_poly, name='add_claim_poly.html'),
    path('claim_location/<str:pk>/add/', views.claim_loc, name='add_claim_loc.html'),
    path('field_proforma/<str:pk>/new/', views.field_proforma_new, name='investor/field_proforma_new.html'),
    path('field_proforma/<str:pk>/detail/', views.field_proforma_detail, name='investor/proforma_detail.html'),

    path('service_provider/face/<str:pk>/detail/', views.service_face_detail, name='services/provider_face_detail.html'),
    path('service_provider/<str:pk>/detail/', views.service_detail, name='services/provider_detail.html'),
    path('add_service_provider/<str:pk>/', views.add_service_provider, name='services/add_provider.html'),
    path('service_provider_list/', views.service_provider_list, name='services/provider_list.html'),
    path('investorview/service_provider/<str:pk>/detail/', views.investview_service_detail, name='investor/investview/provider_detail.html'),

    path('service_history/<str:pk>/detail/', views.service_history_detail, name='services/work_history_detail.html'),
    path('proview_service_history/<str:pk>/detail/', views.proview_service_history_detail, name='services/proview/work_history_detail.html'),
    path('mineview_service_history/<str:pk>/detail/', views.mineview_service_history_detail, name='mine_owner/work_history_detail.html'),
    path('investorview_service_history/<str:pk>/detail/', views.investview_service_history_detail, name='investor/work_history_detail.html'),

    path('mine_owner/<str:pk>/detail/', views.mine_owner_face_detail, name='mine_owner/face_detail.html'),
    path('mine_owner/detail/', views.mine_owner_mines, name='mine_owner/mines.html'),
    path('add_mine_owner/<str:pk>/', views.add_mine_owner, name='mine_owner/add.html'),
    path('mine_owner_list/', views.mine_owner_list, name='mine_owner/list.html'),

    path('mine_owner/mine/<str:pk>/detail/', views.mine_owner_mineview, {'template': 'mine_owner/mineview.html'}, name='mine_owner/mineview.html'),
    path('mine_owner/mine/<str:pk>/field/', views.mine_owner_mineview, {'template': 'mine_owner/mineview_field.html'}, name='mine_owner/mineview/field.html'),
    path('mine_owner/mine/<str:pk>/reports/', views.mine_owner_mineview, {'template': 'mine_owner/mineview_reports.html'}, name='mine_owner/mineview/reports.html'),
    path('mine_owner/mine/<str:pk>/map/', views.mine_owner_mineview, {'template': 'mine_owner/mine_map.html'}, name='mine_owner/mine_map.html'),
    path('mine_owner/mineview/<str:pk>/erp/', views.mineview_erp, name='mine_owner/mineview/erp.html'),
    path('mine_owner/claim/<str:pk>/detail/', views.mine_owner_claimview, {'template': 'mine_owner/claim_detail.html'}, name='mine_owner/claim_detail.html'),
    path('mine_owner/claim/<str:pk>/map/', views.mine_owner_claimview, {'template': 'mine_owner/mining_claim_map.html'}, name='mine_owner/mining_claim_map.html'),
    path('investorview/claim/<str:pk>/map/', views.mine_owner_claimview, {'template': 'investor/mining_claim_map.html'}, name='investor/mining_claim_map.html'),
    path('mine_owner/<str:pk>/mines/', views.mine_owner_mines, name='mine_owner/mandate_detail.html'),
    path('mine_owner/profile/', views.mine_owner_profile, name='mine_owner/profile.html'),
    path('mine_owner/accounts/', views.mine_owner_accounts, name='mine_owner/accounts.html'),

    path('mine_owner/archive/letters/', views.mineview_archive, {'template': 'mine_owner/minewiew/archive/letters.html'}, name='mine_owner/mineview_archive_letters.html'),
    path('mine_owner/archive/agreements/', views.mineview_archive, {'template': 'mine_owner/minewiew/archive/agreements.html'}, name='mine_owner/minewiew_archive_agreements.html'),
    path('mine_owner/archive/receipts/', views.mineview_archive, {'template': 'mine_owner/minewiew/archive/receipts.html'}, name='mine_owner/minewiew_archive_receipts.html'),
    path('mine_owner/archive/others/', views.mineview_archive, {'template': 'mine_owner/minewiew/archive/others.html'}, name='mine_owner/minewiew_archive_others.html'),

    path('provider/profile/', views.provider_profile, name='services/proview/profile.html'),
    path('provider/accounts/', views.proview_accounts, name='services/proview/accounts.html'),
    path('provider_fieldreq_list/', views.provider_fieldreq_list, name='services/proview/fieldreq/list.html'),
    path('provider_fieldreq_quoted_list/', views.provider_fieldreq_quoted_list, name='services/proview/fieldreq/quoted_list.html'),
    path('provider/fieldreq/<str:pk>/detail/', views.proview_fieldreq_detail, name='services/proview/fieldreq/claims.html'),
    path('provider/fieldreq/<str:pk>/quote/', views.proview_fieldreq_quote, name='services/proview/fieldreq/quote.html'),
    path('provider/fieldreq/<str:pk>/attach/', views.proview_fieldreq_attach, name='services/proview/fieldreq/attach.html'),
    path('provider/field/<str:pk>/detail/', views.proview_field_activity_detail, name='services/proview/field/detail_attach.html'),
    path('provider/field/<str:pk>/acquit/', views.proview_field_activity_acquit, name='services/proview/field/acquit.html'),
    path('provider/field/attachment/<str:pk>/create/', views.proview_field_activity_attach_new, name='services/proview/field/attach_new.html'),
    path('provider/field/<str:pk>/acquit/', views.proview_field_activity_acquit, name='services/proview/field/acquit.html'),
    path('provider/field/attach/<str:pk>/detail/', views.proview_field_attach_detail, name='services/proview/field/attach_detail.html'),
    path('provider/<str:pk>/quote/', views.proview_submit_quote, name='services/proview/submit_quote.html'),
    path('provider/<str:pk>/accept_counter_offer/', views.proview_accept_counter_offer, name='services/proview/accept_counter_offer.html'),

    path('quotation/<str:pk>/detail/', views.quote_detail, name='quote_detail.html'),
    path('investorview/<str:pk>/quotation/', views.investview_field_quotation, name='investor/investview/quote_detail.html'),
    path('investorview/<str:pk>/quote_accept_confirm/', views.investview_quote_accept_confirm, name='investor/investview/quote_accept_confirm.html'),
    path('investorview/<str:pk>/quote_counter/', views.investview_quote_counter, name='investor/investview/quote_counter.html'),
    path('investorview/<str:pk>/field_proforma_pay/', views.investview_field_proforma_pay, name='investor/investview/field_proforma_pay.html'),

    path('mandate-request/<str:pk>/detail/', views.mandate_request_detail, name='investor/mandate_request_detail.html'),
    path('mandate/<str:pk>/detail/', views.investor_mandate_detail, name='investor/mandate_detail.html'),
    path('add_investor/<str:pk>/', views.add_investor, name='investor/add.html'),
    path('investor_list/', views.investor_list, name='investor/list.html'),
    path('investor/profile/', views.investor_profile, name='investor/profile.html'),

    path('mine_report/<str:pk>/detail/', views.mine_report_detail, name='mine_report_detail.html'),
    path('mineview_mine_report/<str:pk>/detail/', views.mineview_mine_report_detail, name='mineowner/report_detail.html'),
    path('investorview_report/<str:pk>/detail/', views.investview_mine_report_detail, name='investor/investview/mine/report_detail.html'),
    path('provider_report/<str:pk>/detail/', views.proview_mine_report_detail, name='services/proview/mine/report_detail.html'),
    path('mine_report-lists/', views.mine_report_list, name='mine_report_list.html'),

    path('mine_certificate/<str:pk>/detail/', views.mine_certificate_detail, name='mine_certificate_detail.html'),
    path('mine_certificate-lists/', views.mine_certificate_list, name='mine_certificate_list.html'),

    path('trxn/<str:pk>/detail/', views.trxn_detail, {'template': 'trxn_detail.html'}, name='trxn_detail.html'),
    path('investor_trxn/<str:pk>/detail/', views.trxn_detail, {'template': 'investor/investview/trxn/detail.html'}, name='investor/investview/trxn/detail.html'),
    path('mine_owner_trxn/<str:pk>/detail/', views.trxn_detail, {'template': 'mine_owner/mineview/detail.html'}, name='mine_owner/mineview/detail.html'),
    path('provider_trxn/<str:pk>/detail/', views.trxn_detail, {'template': 'services/detail.html'}, name='services/detail.html'),
    path('trxn-lists/', views.trxn_list, name='trxn_list.html'),
    path('investoview-trxn-lists/', views.investorview_trxn_list, name='investor/investview/trxn/nav_list.html'),

    path('receipt/<str:pk>/detail/', views.receipt_detail, name='receipt_detail.html'),
    path('receipt_list/', views.receipt_list, name='receipt_list.html'),

    path('invoice/<str:pk>/detail/', views.invoice_detail, name='invoice_detail.html'),
    path('mand_req_invoice/<str:pk>/create/', views.mand_req_invoice_create, name='mand_req_invoice_create.html'),
    path('invoice_list/', views.invoice_list, name='invoice_list.html'),

    path('field_request/<str:pk>/detail/', views.field_request_detail, name='investor/field_request_detail.html'),
    path('field_request/<str:pk>/detail/quote', views.field_request_detail_quote, name='investor/field_request_detail_quote.html'),
    path('field_request_list/', views.field_request_list, name='investor/field_request_list.html'),
    path('field_proforma/<str:pk>/new', views.field_proforma_new, name='field_proforma_new.html'),
    path('field_proforma_list/', views.field_proforma_list, name='field_proforma_list.html'),
    path('mandate_proforma_ready/', views.mandate_proforma_ready, name='mandate_proforma_ready.html'),
    path('field_proforma_ready/', views.field_proforma_ready, name='field_proforma_ready.html'),
    path('support_costs/<str:pk>/new', views.support_costs_new, name='investor/support_costs_new.html'),

    path('more_mine_reports/<str:pk>/', views.more_mine_reports, name='more_mine_reports.html'),
    path('more_mine_attachments/<str:pk>/', views.more_mine_attach, name='more_mine_attach.html'),
    path('mine_attach_report/<str:pk>/', views.mine_attach_report, name='mine_attach_report.html'),
    path('mine_attach_certificate/<str:pk>/', views.mine_attach_certificate, name='mine_attach_certificate.html'),
    path('mine_add_claim/<str:pk>/', views.mine_add_claim, name='mine_add_claim.html'),

    path('field_activity/<str:pk>/attachments_detail/', views.field_active, {'template': 'field_activity_detail.html'}, name='field_activity_detail.html'),
    path('field_activity/<str:pk>/remarks_detail/', views.field_active, {'template': 'field_activity_detail_remarks.html'}, name='field_activity_detail_remarks.html'),
    path('field_activity/<str:pk>/create/', views.field_activity_create, name='investor/field_activity_create.html'),
    path('field_activity/attachment/<str:pk>/create/', views.field_activity_attach_new, name='field_attach_new.html'),
    path('field_activity/<str:pk>/acquit/', views.field_activity_acquit, name='field_acquit.html'),
    path('investorview/field_activity/<str:pk>/create/', views.investview_field_activity_create, name='investor/investview/field/add.html'),
    path('field_activity_list/', views.field_activity_list, name='investor/field_activity_list.html'),
    path('field_costing_list/', views.field_costing_list, name='field_costing_list.html'),

    path('add_individual', views.add_individual, name='add_individual.html'),
    path('individual/<str:pk>/edit/', views.individual_edit, name='individual_edit.html'),
    path('individual/<str:pk>/detail/', views.individual_detail, name='individual_detail.html'),
    path('add_corporate', views.add_corporate, name='add_corporate.html'),
    path('corporate/<str:pk>/edit/', views.corporate_edit, name='corporate_edit.html'),
    path('company/<str:pk>/detail/', views.company_detail, name='company_detail.html'),
    path('add_syndicate', views.add_syndicate, name='add_syndicate.html'),
    path('syndicate/<str:pk>/edit/', views.syndicate_edit, name='syndicate_edit.html'),
    path('syndicate/<str:pk>/detail/', views.syndicate_detail, name='syndicate_detail.html'),

    path('ind_player_new/<str:pk>/', views.ind_player_new, name='ind_player_new.html'),
    path('corp_player_new/<str:pk>/', views.corp_player_new, name='corp_player_new.html'),
    path('synd_player_new/<str:pk>/', views.synd_player_new, name='synd_player_new.html'),
    path('player/<str:pk>/edit/', views.player_edit, name='player_edit.html'),
    path('player_list', views.player_list, name='player_list.html'),

    path('mine_new', views.mine_new, name='mine_new.html'),
    path('mine_list', views.mine_list, name='mine_list.html'),
    path('mine/<str:pk>/edit/', views.mine_edit, name='mine_edit.html'),
    path('mine/<str:pk>/detail/', views.mine_detail, {'template': 'mine_detail_mine.html'}, name='mine_detail_mine.html'),
    path('mine/<str:pk>/mandate_req/detail/', views.mine_detail, {'template': 'mine_detail_mandate_req.html'}, name='mine_detail_mandate_req.html'),
    path('mine/<str:pk>/mandate/detail/', views.mine_detail, {'template': 'mine_detail_mandate.html'}, name='mine_detail_mandate.html'),
    path('mine/<str:pk>/carts/detail/', views.mine_detail, {'template': 'mine_detail_carts.html'}, name='mine_detail_carts.html'),
    path('mine/<str:pk>/field_req/detail/', views.mine_detail, {'template': 'mine_detail_field_req.html'}, name='mine_detail_field_req.html'),
    path('mine/<str:pk>/field_visits/detail/', views.mine_detail, {'template': 'mine_detail_field_visits.html'}, name='mine_detail_field_visits.html'),
    path('mine/<str:pk>/proforma/detail/', views.mine_detail, {'template': 'mine_detail_proforma.html'}, name='mine_detail_proforma.html'),
    path('mine/<str:pk>/invoice/detail/', views.mine_detail, {'template': 'mine_detail_invoice.html'}, name='mine_detail_invoice.html'),
    path('mine/<str:pk>/map/detail/', views.mine_detail, {'template': 'mine_map.html'}, name='mine_map.html'),

    path('mining_claim_new', views.mining_claim_new, name='mining_claim_new.html'),
    path('mining_claim_list', views.mining_claim_list, name='mining_claim_list.html'),
    path('mining_claim/<str:pk>/edit/', views.mining_claim_edit, name='mining_claim_edit.html'),
    path('mining_claim/<str:pk>/detail/', views.mining_claim_detail, {'template': 'mining_claim_detail.html'}, name='mining_claim_detail.html'),
    path('mining_claim_map/<str:pk>/', views.mining_claim_detail, {'template': 'mining_claim_map.html'}, name='mining_claim_map.html'),

    path('mandate_proforma/<str:pk>/new', views.mandate_proforma_new, name='mandate_proforma_new.html'),
    path('mandate_proforma_list', views.mandate_proforma_list, name='mandate_proforma_list.html'),

    path('cash_in/<str:pk>/new', views.cash_in, name='cash_in.html'),
    path('cash_out/<str:pk>/new', views.cash_out, name='cash_out.html'),
    path('cash_in_list', views.cash_list, name='cash_list.html'),
    path('request_service_provider/<str:pk>/', views.request_service_provider, name='investor/request_service_provider.html'),
    path('request_service/<str:pk>/done', views.request_service_done, name='investor/request_service_done.html'),

]