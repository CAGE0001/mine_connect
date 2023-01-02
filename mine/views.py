from calmjs.parse.unparsers.extractor import value
from django.urls import reverse_lazy

from .forms import *
from .filters import *
from django.core.paginator import Paginator
from django.contrib import messages, sessions
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, auth
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from sequences import get_next_value
from .utils import *
import pandas as pd
from .decorators import unauthenticated_user, allowed_users
from datetime import timedelta, timezone, date, datetime
import json
import asyncio
from rest_framework import viewsets
from .serializers import *
from rest_framework_gis import serializers
from django.http import JsonResponse
import kwargs as kwargs
from django.db.models.functions import Now
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import register
from django.utils import timezone
from django.forms import inlineformset_factory
from django.db.models.functions import Concat
from django.contrib.gis.geos import Polygon, Point, GEOSGeometry
from django.db.models import Q

@register.filter
def media(form):
    return form.media


def index(request):
    return render(request, 'index.html')


@login_required(login_url='login.html')
def owner_index(request):

    player = request.user.playeruserrelation_set.all().last().player
    alerts = Alerts.objects.filter(status='Active')
    mines = MineOwnerRelation.objects.filter(owner_id=player.id)
    min_locs = []
    min_loc_count = len(min_locs)
    for min in mines:
        mineloc = MineLocation.objects.filter(name_id=min.mine.id).last()
        min_locs.append(mineloc)

    context = {
        'player': player,
        'alerts': alerts,
        'mines': mines,
        'min_locs': min_locs,
        'min_loc_count': min_loc_count,
    }
    return render(request, 'mine_owner/owner_index.html', context)


@login_required(login_url='login.html')
def investor_index(request):

    player = request.user.playeruserrelation_set.all().last().player
    alerts = Alerts.objects.filter(status='Active')

    context = {
        'player': player,
        'alerts': alerts,
    }
    return render(request, 'investor/investor_index.html', context)


@login_required(login_url='login.html')
def provider_index(request):

    player = request.user.playeruserrelation_set.all().last().player
    alerts = Alerts.objects.filter(status='Active')

    context = {
        'player': player,
        'alerts': alerts,
    }
    return render(request, 'services/provider_index.html', context)


@unauthenticated_user
def login(request):

    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('module_options.html')

        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/')
    else:
        return render(request, 'login.html')


@login_required(login_url='login.html')
def confirm_logout(request):
    cancel = request.META.get('HTTP_REFERER')
    context = {
        'cancel': cancel,
    }
    return render(request, 'confirm_logout.html', context)


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('module_options.html')


@login_required(login_url='login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def module_options(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    logger = PlayerUserRelation.objects.filter(party=request.user).last()
    logger_list = []
    logger_count = len(logger_list)
    if logger.status == 'Active':
        if logger.internal == True:
            logger_list.append('index.html')
        if logger.mine_owner == True:
            logger_list.append('mine_owner/owner_index.html')
        if logger.investor == True:
            logger_list.append('investor/investor_index.html')
        if logger.service_provider == True:
            logger_list.append('services/provider_index.html')
        if logger_count == 1:
            context = {
                'player': player,
                'alerts': alerts,
            }
            return render(request, logger_list[0], context)

        context = {
            'logger': logger,
            'player': player,
            'alerts': alerts,
        }
        return render(request, 'module_options.html', context)

    else:
        messages.info(request, 'Invalid Credentials')
        return redirect('/')




@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_individual(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    individuals = IndRecord.objects.all()
    individuals_filter = IndiRecordFilter(request.GET, queryset=individuals)
    records = individuals_filter.qs

    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = IndividualForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.date_created = Now()
            record = form.save(commit=False)

            if IndRecord.objects.filter(nid=record.nid, nationality=record.nationality).exists():
                messages.info(request, 'Individual already exists')
                context = {
                    'form': form,
                    'filter': individuals_filter,
                    'page_obj': page_obj,
                    'type': 'individual',
                    'cancel': cancel,
                    'alerts': alerts,
                }
                return render(request, 'add_individual.html', context)
            record.author = request.user
            record.save()

            indi = IndRecord.objects.filter(dob=record.dob, nid=record.nid).last()
            for item in record.agents.all():
                IndiAgentRelation.objects.create(individual=indi.id, agent_id=item.id)

            return redirect('add_individual.html')

    else:
        form = IndividualForm()

    context = {
        'form': form,
        'filter': individuals_filter,
        'page_obj': page_obj,
        'type': 'individual',
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'add_individual.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def individual_edit(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    individual = IndRecord.objects.get(pk=pk)
    post = get_object_or_404(IndRecord, pk=pk)
    player = Player.objects.filter(ref=pk, type='Individual')

    if request.method == 'POST':
        form = IndividualEditForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)

            if IndRecord.objects.filter(name=record.nid, nationality=record.nationality).exists() or IndRecord.objects.filter(name=record.reg_number, nationality=record.nationality).exists():
                messages.info(request, 'Individual already exists')
                return render(request, 'individual_edit.html', {'form': form, 'individual': individual, 'player': player})

            if record.dob >= record.date_created - timedelta(years=18):
                messages.info(request, 'Individual too young to be registered')
                return render(request, 'individual_edit.html', {'form': form, 'individual': individual, 'player': player})

            record.save()
            return redirect('player_detail.html', pk=player.id)

    else:
        form = IndividualEditForm(instance=post)

    context = {
        'form': form,
        'individual': individual,
        'player': player,
        'alerts': alerts,
    }
    return render(request, 'individual_edit.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def individual_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    individual = IndRecord.objects.get(pk=pk)
    player = Player.objects.filter(ref=pk, type='Individual')

    context = {
        'indi': individual,
        'alerts': alerts,
    }
    return render(request, 'individual_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def company_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    company = CorpRecord.objects.get(pk=pk)
    player = Player.objects.filter(ref=pk, type='Company')

    context = {
        'corp': company,
        'alerts': alerts,
    }
    return render(request, 'company_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def syndicate_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    syndicate = Syndicate.objects.get(pk=pk)
    player = Player.objects.filter(ref=pk, type='Syndicate')

    context = {
        'synd': syndicate,
        'alerts': alerts,
    }
    return render(request, 'syndicate_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def syndicate_edit(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    syndicate = Syndicate.objects.get(pk=pk)
    post = get_object_or_404(Syndicate, pk=pk)
    player = Player.objects.filter(ref=pk, type='Syndicate').last()

    if request.method == 'POST':
        form = SyndicateEditForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)

            if Syndicate.objects.filter(name=record.name):
                messages.info(request, 'Syndicate already exists')
                return render(request, 'syndicate_edit.html', {'form': form, 'syndicate': syndicate, 'player': player})

            record.save()
            return redirect('player_detail.html',  pk=player.id)

    else:
        form = SyndicateEditForm(instance=post)

    context = {
        'form': form,
        'player': player,
        'syndicate': syndicate,
        'alerts': alerts,
    }
    return render(request, 'syndicate_edit.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def corporate_edit(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    corporate = CorpRecord.objects.get(pk=pk)
    post = get_object_or_404(CorpRecord, pk=pk)
    player = Player.objects.filter(ref=pk, type='Corporate').last()

    if request.method == 'POST':
        form = CorporateEditForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)

            if CorpRecord.objects.filter(reg_number=record.reg_number, nationality=record.nationality):
                messages.info(request, 'Company already exists')
                return render(request, 'syndicate_edit.html', {'form': form, 'corporate': corporate, 'player': player})

            record.save()
            return redirect('player_detail.html',  pk=player.id)

    else:
        form = CorporateEditForm(instance=post)

    context = {
        'form': form,
        'player': player,
        'corporate': corporate,
        'alerts': alerts,
    }
    return render(request, 'corporate_edit.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_corporate(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    companies = CorpRecord.objects.all()
    company_filter = CorpRecordFilter(request.GET, queryset=companies)
    records = company_filter.qs

    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    corp = None

    if request.method == 'POST':
        form = CorporateForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.date_created = Now()
            record = form.save(commit=False)

            if CorpRecord.objects.filter(name=record.name, nationality=record.nationality).exists() or CorpRecord.objects.filter(name=record.reg_number, nationality=record.nationality).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'add_corporate.html', {'form': form, 'filter': company_filter})

            # if record.date_created >= record.date_created:
            #     messages.info(request, 'Company date of registration defective')
            #     return render(request, 'add_corporate.html', {'form': form, 'filter': company_filter})

            record.author = request.user
            record.save()

            corp = CorpRecord.objects.filter(name=record.name, reg_number=record.reg_number).last()
            for item in record.agents.all():
                CorpAgentRelation.objects.create(company=corp.id, agent_id=item.id)

            return redirect('add_corporate.html')

    else:
        form = CorporateForm()

    context = {
        'form': form,
        'filter': company_filter,
        'page_obj': page_obj,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'add_corporate.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_syndicate(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    syndicates = Syndicate.objects.all()
    syndicate_filter = SyndRecordFilter(request.GET, queryset=syndicates)
    records = syndicate_filter.qs

    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    synd = None

    if request.method == 'POST':
        form = SyndicateForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.date_created = Now()
            record = form.save(commit=False)

            if Syndicate.objects.filter(name=record.name).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'add_syndicate.html', {'form': form, 'filter': syndicate_filter})
            record.author = request.user
            record.save()

            synd = Syndicate.objects.filter(name=record.name, dor=record.dor).last()
            for item in record.agents.all():
                SyndAgentRelation.objects.create(syndicate=synd.id, agent_id=item.id)
            for item in record.member.all():
                SyndMemberRelation.objects.create(syndicate=synd.id, member_id=item.id)

            return redirect('add_syndicate.html', )

    else:
        form = SyndicateForm()

    context = {
        'form': form,
        'filter': syndicate_filter,
        'page_obj': page_obj,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'add_syndicate.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def ind_player_new(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    indi = IndRecord.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')
    post = get_object_or_404(IndRecord, id=pk)

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        form1 = IndiStatUpdate(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            record.ref = pk
            record.name = indi.first_name + " " + indi.last_name
            record.type = 'Individual'
            record = form.save(commit=False)

            if Player.objects.filter(type=record.type, ref=pk).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'ind_player_new.html', {'form': form})

            record.date_created = Now()
            record.payment_date = Now()
            record.author = request.user
            record.save()

            if form1.is_valid():
                form1.status = 'Done'
                form1.save()

                return redirect('player_list.html')

    else:
        form = PlayerForm()
        form1 = IndiStatUpdate(instance=post)

    context = {
        'indi': indi,
        'form': form,
        'form1': form1,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'ind_player_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def player_individuals_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = IndRecord.objects.filter(status='None')
    filter = PlayerIndFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'individuals_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def player_company_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = CorpRecord.objects.filter(status='None')
    filter = PlayerCorpFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'company_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_mandate_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    investor = player.investor_set.all().last()
    cart_requests = CartRequest.objects.filter(investor=investor)
    filter_mandates = Mandate.objects.filter(mandate_request__cart_mine_match__cart_request__investor=investor)
    filter = MandateListFilter(request.GET, queryset=filter_mandates)
    filter_mandates = filter.qs
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    mandate_list = []
    mandate_count = len(mandate_list)
    mandate_requests = None
    mandate = None
    if cart_requests:
        for cart_request in cart_requests:
            cart_mine_matches = cart_request.cartminematch_set.all()
            if cart_mine_matches:
                for cart_mine_match in cart_mine_matches:
                    mandate_requests = cart_mine_match.mandaterequest_set.all()
                    if mandate_requests:
                        for mandate_request in mandate_requests:
                            mandate = Mandate.objects.filter(mandate_request=mandate_request).last()
                            if mandate:
                                mandate_list.append(mandate)

    context = {
        'filter': filter,
        'page_obj': page_obj,
        'mandate_list': mandate_list,
        'mandate_count': mandate_count,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/mandate/list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_field_request_list(request):

    player = request.user.playeruserrelation_set.all().last().player
    alerts = Alerts.objects.filter(player=player)
    investor = player.investor_set.all().last()
    cart_requests = CartRequest.objects.filter(investor_id=investor.id)
    filter_requests = FieldReq.objects.filter(mandate__mandate_request__cart_mine_match__cart_request__investor=investor)
    filter = InvestorFieldReqFilter(request.GET, queryset=filter_requests)
    filter_requests = filter.qs
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    request_list = []
    request_count = len(request_list)
    mandate_requests = 0
    mandate = 0
    field_request = 0
    if cart_requests:
        for cart_request in cart_requests:
            cart_mine_matches = cart_request.cartminematch_set.all()
            if cart_mine_matches:
                for cart_mine_match in cart_mine_matches:
                    mandate_requests = cart_mine_match.mandaterequest_set.all()
                    if mandate_requests:
                        for mandate_request in mandate_requests:
                            mandates = mandate_request.mandate_set.all()
                            for mandate in mandates:
                                field_requests = mandate.fieldreq_set.all()
                                if field_requests:
                                    for field_request in field_requests:
                                        request_list.append(field_request)

    context = {
        'filter': filter,
        'page_obj': page_obj,
        'request_list': request_list,
        'mandate_count': request_count,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/fieldreq/list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def player_syndicate_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = Syndicate.objects.filter(status='None')
    filter = PlayerSyndFilter(request.GET, queryset=records)

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'syndicate_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mandate_proforma_list(request):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    records = MandateProforma.objects.all()
    filter = MandateProformaFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'mandate_proforma_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def corp_player_new(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    corp = CorpRecord.objects.get(id=pk)
    post = get_object_or_404(CorpRecord, id=pk)

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        form1 = CorpStatUpdate(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            record.ref = pk
            record.name = corp.name + " " + corp.type
            record.type = 'Corporate'
            record = form.save(commit=False)

            if Player.objects.filter(type=record.type, ref=pk).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'corp_player_new.html', {'form': form})

            record.date_created = Now()
            record.payment_date = Now()
            record.author = request.user
            record.save()

            if form1.is_valid():
                form1.status = 'Done'
                form1.save()

                return redirect('player_list.html')

    else:
        form = PlayerForm()
        form1 = CorpStatUpdate(instance=post)

    context = {
        'corp': corp,
        'form': form,
        'form1': form1,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'corp_player_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def synd_player_new(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    synd = Syndicate.objects.get(id=pk)
    post = get_object_or_404(Syndicate, id=pk)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        form1 = SyndStatUpdate(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            record.ref = pk
            record.name = synd.name
            record.type = 'Syndicate'
            record = form.save(commit=False)

            if Player.objects.filter(type=record.type, ref=pk).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'synd_player_new.html', {'form': form})

            record.date_created = Now()
            record.payment_date = Now()
            record.author = request.user
            record.save()

            if form1.is_valid():
                form1.status = 'Done'
                form1.save()

                return redirect('player_list.html')

    else:
        form = PlayerForm()
        form1 = SyndStatUpdate(instance=post)

    context = {
        'synd': synd,
        'form': form,
        'form1': form1,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'synd_player_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_cart_request_new(request, pk):

    cancel = request.META.get('HTTP_REFERER')
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    investor = player.investor_set.all().last()

    if request.method == 'POST':
        form = CartRequestForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.investor_id = investor.id
            record = form.save(commit=False)

            if CartRequest.objects.filter(investor_id=record.investor.id, mineral=record.mineral, location=record.location).exists():
                messages.info(request, 'Request already exists')
                return render(request, 'investor/investview/cart/request.html', {'form': form})

            record.date_created = Now()
            record.author = request.user
            record.save()

            return redirect('investor/investview/cart/lists.html')

    else:
        form = CartRequestForm()

    context = {
        'investor': investor,
        'form': form,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/cart/request.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def player_edit(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = Player.objects.get(pk=pk)
    post = get_object_or_404(Player, pk=pk)

    if request.method == 'POST':
        form = PlayerEditForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            record.save()
            return redirect('player_detail.html',  pk=player.id)

    else:
        form = PlayerEditForm(instance=post)

    context = {
        'form': form,
        'player': player,
        'alerts': alerts,
    }
    return render(request, 'player_edit.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_new(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    mine = None
    if request.method == 'POST':
        form = NewMineForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.date_created = Now()
            record = form.save(commit=False)

            if Mine.objects.filter(name=record.name).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'mine_new.html', {'form': form})
            record.author = request.user
            record.save()
            mine = Mine.objects.filter(name=record.name).last()
            for item in record.mineral.all():
                MineMineral.objects.create(mine_id=record.mine.id, mineral_id=item.id, author=request.user)

            return redirect('mine_list.html')

    form = NewMineForm()

    context = {
        'form': form,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'mine_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_edit(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    post = get_object_or_404(Mine, pk=pk)

    if request.method == 'POST':
        form = NewMineForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)

            if Mine.objects.filter(name=record.name, owner=record.owner).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'mine_new.html', {'form': form})
            record.save()
            return redirect('mine_detail_mine.html', pk=pk)

    else:
        form = NewMineForm()

    context = {
        'form': form,
        'alerts': alerts,
    }
    return render(request, 'mine_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mineview_production_mineral(request, pk, template):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    mineral_production = []
    ore_production = []
    waste_production = []
    products = mine.mineproduction_set.all()
    mineral_count = len(products.filter(material='Mineral'))
    ore_count = len(products.filter(material='Ore'))
    waste_count = len(products.filter(material='Waste'))
    filter = MoreProductionFilter(request.GET, queryset=products)
    products = filter.qs
    minerals = 0
    ore = 0
    waste = 0

    if products.filter(material='Mineral'):
        minerals = products.filter(material='Mineral')
        for prod in minerals:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in mineral_production:
                if item:
                    if produce[0] == item[0]:
                        mineral_production[n][1] = item[1] + produce[1]
                    else:
                        mineral_production.append(produce)
                else:
                    mineral_production.append(produce)
                n += 1

    if products.filter(material='Ore'):
        ore = products.filter(material='Ore')
        for prod in ore:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in ore_production:
                if item:
                    if produce[0] == item[0]:
                        ore_production[n][1] = item[1] + produce[1]
                    else:
                        ore_production.append(produce)
                else:
                    ore_production.append(produce)
                n += 1

    if products.filter(material='Waste'):
        waste = products.filter(material='Waste')
        for prod in waste:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in waste_production:
                if item:
                    if produce[0] == item[0]:
                        waste_production[n][1] = item[1] + produce[1]
                    else:
                        waste_production.append(produce)
                else:
                    waste_production.append(produce)
                n += 1

    context = {
        'mine': mine,
        'filter': filter,
        'mineral_count': mineral_count,
        'ore_count': ore_count,
        'waste_count': waste_count,
        'mineral_production': mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'minerals': minerals,
        'ore': ore,
        'waste': waste,
        'alerts': alerts,
    }
    return render(request, 'mineview_production_mineral.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mineview_production_ore(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    mineral_production = []
    ore_production = []
    waste_production = []
    products = mine.mineproduction_set.all()
    mineral_count = len(products.filter(material='Mineral'))
    ore_count = len(products.filter(material='Ore'))
    waste_count = len(products.filter(material='Waste'))
    filter = MoreProductionFilter(request.GET, queryset=products)
    products = filter.qs
    minerals = 0
    ore = 0
    waste = 0

    if products.filter(material='Mineral'):
        minerals = products.filter(material='Mineral')
        for prod in minerals:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in mineral_production:
                if item:
                    if produce[0] == item[0]:
                        mineral_production[n][1] = item[1] + produce[1]
                    else:
                        mineral_production.append(produce)
                else:
                    mineral_production.append(produce)
                n += 1

    if products.filter(material='Ore'):
        ore = products.filter(material='Ore')
        for prod in ore:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in ore_production:
                if item:
                    if produce[0] == item[0]:
                        ore_production[n][1] = item[1] + produce[1]
                    else:
                        ore_production.append(produce)
                else:
                    ore_production.append(produce)
                n += 1

    if products.filter(material='Waste'):
        waste = products.filter(material='Waste')
        for prod in waste:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in waste_production:
                if item:
                    if produce[0] == item[0]:
                        waste_production[n][1] = item[1] + produce[1]
                    else:
                        waste_production.append(produce)
                else:
                    waste_production.append(produce)
                n += 1

    context = {
        'mine': mine,
        'filter': filter,
        'mineral_count': mineral_count,
        'ore_count': ore_count,
        'waste_count': waste_count,
        'mineral_production': mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'minerals': minerals,
        'ore': ore,
        'waste': waste,
        'alerts': alerts,
    }
    return render(request, 'mineview_production_ore.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mineview_production_waste(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    mineral_production = []
    ore_production = []
    waste_production = []
    products = mine.mineproduction_set.all()
    mineral_count = len(products.filter(material='Mineral'))
    ore_count = len(products.filter(material='Ore'))
    waste_count = len(products.filter(material='Waste'))
    filter = MoreProductionFilter(request.GET, queryset=products)
    products = filter.qs
    minerals = 0
    ore = 0
    waste = 0

    if products.filter(material='Mineral'):
        minerals = products.filter(material='Mineral')
        for prod in minerals:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in mineral_production:
                if item:
                    if produce[0] == item[0]:
                        mineral_production[n][1] = item[1] + produce[1]
                    else:
                        mineral_production.append(produce)
                else:
                    mineral_production.append(produce)
                n += 1

    if products.filter(material='Ore'):
        ore = products.filter(material='Ore')
        for prod in ore:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in ore_production:
                if item:
                    if produce[0] == item[0]:
                        ore_production[n][1] = item[1] + produce[1]
                    else:
                        ore_production.append(produce)
                else:
                    ore_production.append(produce)
                n += 1

    if products.filter(material='Waste'):
        waste = products.filter(material='Waste')
        for prod in waste:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in waste_production:
                if item:
                    if produce[0] == item[0]:
                        waste_production[n][1] = item[1] + produce[1]
                    else:
                        waste_production.append(produce)
                else:
                    waste_production.append(produce)
                n += 1

    context = {
        'mine': mine,
        'filter': filter,
        'mineral_count': mineral_count,
        'ore_count': ore_count,
        'waste_count': waste_count,
        'mineral_production': mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'minerals': minerals,
        'ore': ore,
        'waste': waste,
        'alerts': alerts,
    }
    return render(request, 'mineview_production_waste.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def more_production_reports(request, pk, template):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    mine = Mine.objects.get(id=pk)
    mineloc = MineLocation.objects.filter(name_id=mine.id).last()
    polygon = mine.minepolygon_set.all().last()
    mineral_production = []
    ore_production = []
    waste_production = []
    products = mine.mineproduction_set.all()
    mineral_count = len(products.filter(material='Mineral'))
    ore_count = len(products.filter(material='Ore'))
    waste_count = len(products.filter(material='Waste'))
    filter = MoreProductionFilter(request.GET, queryset=products)
    products = filter.qs
    minerals = 0
    ore = 0
    waste = 0
    works = None
    labour = None
    plant = None
    mobile = None

    if products.filter(material='Mineral'):
        minerals = products.filter(material='Mineral')
        for prod in minerals:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in mineral_production:
                if item:
                    if produce[0] == item[0]:
                        mineral_production[n][1] = item[1] + produce[1]
                    else:
                        mineral_production.append(produce)
                else:
                    mineral_production.append(produce)
                n += 1
        records = minerals
        paginator = Paginator(records, 10)
        page_number = request.GET.get('page')
        minerals = paginator.get_page(page_number)

    if products.filter(material='Ore'):
        ore = products.filter(material='Ore')
        for prod in ore:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in ore_production:
                if item:
                    if produce[0] == item[0]:
                        ore_production[n][1] = item[1] + produce[1]
                    else:
                        ore_production.append(produce)
                else:
                    ore_production.append(produce)
                n += 1
        records = ore
        paginator = Paginator(records, 10)
        page_number = request.GET.get('page')
        ore = paginator.get_page(page_number)

    if products.filter(material='Waste'):
        waste = products.filter(material='Waste')
        for prod in waste:
            produce = [prod.mineral, prod.quantity]
            n = 0
            for item in waste_production:
                if item:
                    if produce[0] == item[0]:
                        waste_production[n][1] = item[1] + produce[1]
                    else:
                        waste_production.append(produce)
                else:
                    waste_production.append(produce)
                n += 1
        records = waste
        paginator = Paginator(records, 10)
        page_number = request.GET.get('page')
        waste = paginator.get_page(page_number)

    if mine.mineworks_set.all():
        works = mine.mineworks_set.all()
        works_filter = MineviewWorksFilter(request.GET, queryset=works)
        works = works_filter.qs
        records = works
        paginator = Paginator(records, 10)
        page_number = request.GET.get('page')
        works = paginator.get_page(page_number)
    if mine.minelabour_set.all():
        labour = mine.minelabour_set.all().last()
    if mine.mineplant_set.all():
        plant = mine.mineplant_set.all()
        plant_filter = MineviewPlantFilter(request.GET, queryset=plant)
        plant = plant_filter.qs
        records = plant
        paginator = Paginator(records, 10)
        page_number = request.GET.get('page')
        plant = paginator.get_page(page_number)
    if mine.mineyellowplant_set.all():
        mobile = mine.mineyellowplant_set.all()
        mobile_filter = MineviewMobileFilter(request.GET, queryset=mobile)
        mobile = mobile_filter.qs
        records = mobile
        paginator = Paginator(records, 10)
        page_number = request.GET.get('page')
        mobile = paginator.get_page(page_number)

    context = {
        'mine': mine,
        'poly': polygon,
        'mineloc': mineloc,
        'filter': filter,
        'mineral_count': mineral_count,
        'ore_count': ore_count,
        'waste_count': waste_count,
        'mineral_production': mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'minerals': minerals,
        'ore': ore,
        'waste': waste,
        'works': works,
        'labour': labour,
        'plant': plant,
        'mobile': mobile,
        'alerts': alerts,
        'cancel': cancel,
    }
    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def more_mine_reports(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    reports = mine.minereports_set.all()
    report_count = len(reports)
    attachments = mine.minecertificates_set.all()
    attach_count = len(attachments)
    filter = MineReportFilter(request.GET, queryset=reports)

    context = {
        'mine': mine,
        'filter': filter,
        'report_count': report_count,
        'attach_count': attach_count,
        'alerts': alerts,
    }
    return render(request, 'more_mine_reports.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def more_mine_attach(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    attachments = mine.minecertificates_set.all()
    attach_count = len(attachments)
    reports = mine.minereports_set.all()
    report_count = len(reports)
    filter = MineReportFilter(request.GET, queryset=attachments)

    context = {
        'mine': mine,
        'filter': filter,
        'attach_count': attach_count,
        'report_count': report_count,
        'alerts': alerts,
    }
    return render(request, 'more_mine_attach.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_attach_report(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AttachReportForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            if MineReports.objects.filter(mine_id=mine.id, type=record.type, report_date=record.report_date).exists():
                messages.info(request, 'Report already Exists')
                redirect(cancel)
            record.author = request.user
            record.date_created = Now()
            record.save()

            return redirect(cancel)

    form = AttachReportForm()
    context = {
        'mine': mine,
        'form': form,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'mine_attach_report.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_attach_certificate(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AttachCertForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            if MineCertificates.objects.filter(mine=record.mine, type=record.type, issue_date=record.issue_date).exists():
                messages.info(request, 'Certificate already Exists')
                redirect(cancel)
            record.author = request.user
            record.date_created = Now()
            record.save()

        return redirect(cancel)

    form = AttachCertForm()
    context = {
        'mine': mine,
        'form': form,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'mine_attach_certificate.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def attach_letter(request, pk):

    player = Player.objects.get(id=pk)
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AttachLetterForm(request.POST, request.FILES, player=player)
        if form.is_valid():
            record = form.save(commit=False)
            record.player_id = player.id
            if MineLetters.objects.filter(mine_id=record.mine_id, type=record.type, report_date=record.report_date, other_party=record.other_party, subject=record.subject).exists():
                messages.info(request, 'Report already Exists')
                redirect(player_detail.html, pk=player.id)
            record.author = request.user
            record.date_created = Now()
            record.save()

        return redirect(player_detail.html, pk=player.id)

    form = AttachLetterForm(player=player)
    context = {
        'player': player,
        'form': form,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'add_letter.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def attach_receipt(request, pk):

    player = Player.objects.get(id=pk)
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AttachReceiptForm(request.POST, request.FILES, player=player)
        if form.is_valid():
            record = form.save(commit=False)
            record.player_id = player.id
            if MineReceipts.objects.filter(mine_id=record.mine_id, type=record.type, report_date=record.report_date, issued_by=record.issued_by, rec_number=record.rec_number).exists():
                messages.info(request, 'Report already Exists')
                redirect(player_detail.html, pk=player.id)
            record.author = request.user
            record.date_created = Now()
            record.save()
        return redirect(player_detail.html, pk=player.id)

    form = AttachReceiptForm(player=player)
    context = {
        'player': player,
        'form': form,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'add_receipt.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def attach_agreement(request, pk):

    player = Player.objects.get(id=pk)
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    object = None
    if request.method == 'POST':
        form = AttachAgreementForm(request.POST, request.FILES, player=player)
        if form.is_valid():
            record = form.save(commit=False)
            record.player_id = player.id
            if MineAgreements.objects.filter(mine_id=record.mine_id, type=record.type, report_date=record.report_date, counter_party=record.counter_party).exists():
                messages.info(request, 'Report already Exists')
                redirect(player_detail.html, pk=player.id)
            record.author = request.user
            record.date_created = Now()
            record.save()

            if record.addendum == True:
                object = MineAgreements.objects.filter(mine_id=record.mine_id, type=record.type, report_date=record.report_date, counter_party=record.counter_party).last()
                MineAgreementAddendum.objects.Create(principal_id=record.addendum, addendum=object.id)

        return redirect(cancel)

    form = AttachAgreementForm(player=player)
    context = {
        'player': player,
        'form': form,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'add_agreement.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def attach_other_doc(request, pk):

    player = Player.objects.get(id=pk)
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AttachOtherDocForm(request.POST, request.FILES, player=player)
        if form.is_valid():
            record = form.save(commit=False)
            record.player_id = player.id
            if OtherDocs.objects.filter(mine_id=record.mine_id, report_date=record.report_date, subject=record.subject).exists():
                messages.info(request, 'Report already Exists')
                redirect(cancel)
            record.author = request.user
            record.date_created = Now()
            record.save()

        return redirect(cancel)

    form = AttachOtherDocForm(player=player)
    context = {
        'player': player,
        'form': form,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'add_other_doc.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_add_claim(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    post = None
    if request.method == 'POST':
        form = MineClaimForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            if MineClaimRelation.objects.filter(claim_id=record.claim_id).exists():
                messages.info(request, 'Mining Claim already Exists')
                return render(request, 'mine_add_claim.html', {'form': form})
            record.author = request.user
            record.date_created = Now()
            record.save()
            post = get_object_or_404(MiningClaim, id=record.claim_id)
            form1 = ClaimStatusForm(request.POST, instance=post)
            if form1.is_valid():
                form1 = form1.save(commit=False)
                form1.status = 'Attached'
                form1.save()

            return redirect('mine_detail_mine.html', pk=mine.id)

    form = MineClaimForm()
    form1 = ClaimStatusForm(instance=post)
    context = {
        'mine': mine,
        'form': form,
        'form1': form1,
        'alerts': alerts,
    }
    return render(request, 'mine_add_claim.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def claim_reg_cert_add(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    claim = MiningClaim.objects.get(id=pk)
    if request.method == 'POST':
        form = AttachClaimCertForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.claim_id = claim.id
            if ClaimRegCert.objects.filter(claim_id=record.claim_id).exists():
                messages.info(request, 'Certificate already Exists')
                context = {
                    'claim': claim,
                    'form': form,
                    'cancel': cancel,
                    'alerts': alerts,
                }
                return render(request, 'claim_reg_cert_add.html', context)
            record.author = request.user
            record.date_created = Now()
            record.save()
        return redirect('mining_claim_detail.html', pk=claim.id)

    form = AttachClaimCertForm()
    context = {
        'claim': claim,
        'form': form,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'claim_reg_cert_add.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_mine_detail(request, pk, template):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    cancel = request.META.get('HTTP_REFERER')
    mine = Mine.objects.get(id=pk)
    mineloc = MineLocation.objects.filter(name_id=mine.id).last()
    polygon = mine.minepolygon_set.all().last()
    reports = mine.minereports_set.all()[:2]
    attachments = mine.minecertificates_set.all()[:2]
    visit_requests_list = []
    visit_req_count = len(visit_requests_list)
    field_proforma_list = []
    field_proforma_count = len(field_proforma_list)
    visit_list = []
    visit_count = len(visit_list)
    field_invoice_list = []
    field_invoice_count = len(field_invoice_list)
    mandate_list = []
    mandate_count = len(mandate_list)
    mandate_request_list = []
    mandate_request_count = len(mandate_request_list)

    claims = MineClaimRelation.objects.filter(mine=mine)
    mine_area = 0
    for claim in claims:
        area =  claim.claim.area
        mine_area += area
    claims_filter = ClaimsFilter(request.GET, queryset=claims)
    minerals = MineMineral.objects.filter(mine_id=pk)
    cart_matches = CartMineRelation.objects.filter(mine=mine)
    cart_filter = CartMatchFilter(request.GET, queryset=claims)
    cart_match_count = cart_matches.count
    production = None
    works = None
    labour = None
    plant = None
    mobile = None
    mineral_production = []
    ore_production = 0
    waste_production = 0
    mineral_set = ['all',]
    units_set = []
    i = 0
    if mine.mineproduction_set.all():
        production = mine.mineproduction_set.all()
        for prod in production:
            if prod.mineral not in mineral_set:
                mineral_set.append(prod.mineral)
                mineral_production.append([prod.mineral, prod.quantity, prod.unit])
            else:
                i = mineral_set.index(prod.mineral)
                if prod.material == 'mineral':
                    if prod.mineral != 'all':
                        mineral_production[i][1] = mineral_production[i][1] + prod.quantity
                    else:
                        if prod.material == 'ore':
                            ore_production =+ prod.quantity
                        else:
                            waste_production =+ prod.quantity

    if mine.mineworks_set.all():
        works = mine.mineworks_set.all()
    if mine.minelabour_set.all():
        labour = mine.minelabour_set.all().last()
    if mine.mineplant_set.all():
        plant = mine.mineplant_set.all()
    if mine.mineyellowplant_set.all():
        mobile = mine.mineyellowplant_set.all()

    mandate_match = 0
    mandate = 0
    visit_req = 0
    if cart_matches:
        for cart_match in cart_matches:
            mandate_match = MineMandateRequest.objects.filter(mandate_request=cart_match.cart.mandaterequest_set.all().last(), mine=mine).last()
            if mandate_match:
                mandate_request_list.append([cart_match, mandate_match])
                mandate = mandate_match.mandate_request.mandate_set.all().last()
                if mandate:
                    mandate_list.append([cart_match, mandate_match, mandate])
                    visit_requests = FieldReq.objects.filter(mandate=mandate)
                    visit_request_filter = FieldReqFilter(request.GET, queryset=visit_requests)
                    visit_requests = visit_request_filter.qs
                    visit_req_count = visit_requests.count
                    if visit_requests:
                        for visit_req in visit_requests:
                            field_proforma = FieldProforma.objects.filter(field_request=visit_req).last()
                            visit_requests_list.append([cart_match, mandate_match, mandate, visit_req])
                            if field_proforma:
                                field_invoice = FieldInvoice.objects.filter(field_proforma=field_proforma).last()
                                visit = Field.objects.filter(proforma=field_proforma).last()
                                field_proforma_list.append([cart_match, mandate_match, mandate, visit_req,
                                                           field_proforma])
                                if field_invoice:
                                    field_invoice_list.append([cart_match, mandate_match, mandate, visit_req,
                                                              field_proforma, field_invoice])
                                if visit:
                                    visit_list.append([cart_match, mandate_match, mandate, visit_req, field_proforma,
                                                      visit])

    context = {
        'mine': mine,
        'poly': polygon,
        'mineloc': mineloc,
        'claims_filter': claims_filter,
        'minerals': minerals,
        'mandate_count': mandate_count,
        'visit_req_count': visit_req_count,
        'cart_match_count': cart_match_count,
        'visit_count': visit_count,
        'field_proforma_count': field_proforma_count,
        'visit_requests_list': visit_requests_list,
        'field_proforma_list': field_proforma_list,
        'visit_list': visit_list,
        'field_invoice_list': field_invoice_list,
        'field_invoice_count': field_invoice_count,
        'mandate_list': mandate_list,
        'mandate_request_list': mandate_request_list,
        'mandate_request_count': mandate_request_count,
        'filter': cart_filter,
        'production': production,
        'works': works,
        'labour': labour,
        'plant': plant,
        'mobile': mobile,
        'reports': reports,
        'attachments': attachments,
        'mineral_production':mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'mineral_set': mineral_set,
        'units_set': units_set,
        'mine_area': mine_area,
        'alerts': alerts,
        'cancel': cancel,
    }
    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_detail(request, pk, template):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    mine = Mine.objects.get(id=pk)
    sample_points = SamplePoint.objects.filter(mine=mine)
    mine_area = 0
    mineloc = MineLocation.objects.filter(name_id=mine.id).last()
    polygon = mine.minepolygon_set.all().last()
    works_filter = None
    plant_filter = None
    mobile_filter = None

    reports = mine.minereports_set.all()[:2]
    attachments = mine.minecertificates_set.all()[:2]
    visit_requests_list = []
    visit_req_count = len(visit_requests_list)
    field_proforma_list = []
    field_proforma_count = len(field_proforma_list)
    visit_list = []
    visit_count = len(visit_list)
    field_invoice_list = []
    field_invoice_count = len(field_invoice_list)
    mandate_list = []
    mandate_count = len(mandate_list)
    mandate_request_list = []
    mandate_request_count = len(mandate_request_list)
    mandate_req_status = None
    obj = None
    if mandate_request_list:
        for req in mandate_request_list:
            obj = MineMandateRequest.objects.filter(mandate_request_id=req[1].id)
            mandate_req_status = obj.last().status

    claims = MineClaimRelation.objects.filter(mine=mine)
    claims_filter = ClaimsFilter(request.GET, queryset=claims)
    claims = claims_filter.qs
    claimpoly = []
    for claim in claims:
        mine_area = mine_area + claim.claim.area
        if claim.claim.miningclaimpolygon_set.all():
            polygon = claim.claim.miningclaimpolygon_set.all().last()
            claimpoly.append(polygon)

    cart_matches = CartMineRelation.objects.filter(mine=mine)
    cart_filter = CartMatchFilter(request.GET, queryset=cart_matches)
    cart_match_count = cart_matches.count
    cart_matches = cart_filter.qs
    works = None
    labour = None
    plant = None
    mobile = None
    mineral_production = []
    ore_production = 0
    waste_production = 0
    products = mine.mineproduction_set.all()
    mineral_count = len(products.filter(material='Mineral'))
    ore_count = len(products.filter(material='Ore'))
    waste_count = len(products.filter(material='Waste'))
    filter = MoreProductionFilter(request.GET, queryset=products)
    products = filter.qs
    minerals = 0
    ore = 0
    waste = 0
    mineral_set = ['all',]
    units_set = []
    i = 0
    if mine.mineproduction_set.all():
        production = mine.mineproduction_set.all()
        for prod in production:
            if prod.mineral not in mineral_set:
                mineral_set.append(prod.mineral)
                mineral_production.append([prod.mineral, prod.quantity, prod.unit])
            else:
                i = mineral_set.index(prod.mineral)
                if prod.material == 'mineral':
                    if prod.mineral != 'all':
                        mineral_production[i][1] = mineral_production[i][1] + prod.quantity
                    else:
                        if prod.material == 'ore':
                            ore_production += prod.quantity
                        else:
                            waste_production += prod.quantity

    if mine.mineworks_set.all():
        works = mine.mineworks_set.all()
        works_filter = MineviewWorksFilter(request.GET, queryset=works)
        works = works_filter.qs
    if mine.minelabour_set.all():
        labour = mine.minelabour_set.all().last()
    if mine.mineplant_set.all():
        plant = mine.mineplant_set.all()
        plant_filter = MineviewPlantFilter(request.GET, queryset=plant)
        plant = plant_filter.qs
    if mine.mineyellowplant_set.all():
        mobile = mine.mineyellowplant_set.all()
        mobile_filter = MineviewMobileFilter(request.GET, queryset=mobile)
        mobile = mobile_filter.qs

    mandate_requests = None
    mandate = None
    visit_req = None
    if cart_matches:
        for cart_match in cart_matches:
            mandate_requests = cart_match.cart.mandaterequest_set.all()
            if mandate_requests:
                for mandate_request in mandate_requests:
                    mandate_request_list.append([cart_match, mandate_request])
                    mandate = Mandate.objects.filter(mandate_request=mandate_request).last()
                    if mandate:
                        mandate_list.append([cart_match, mandate_request, mandate])
                        visit_requests = FieldReq.objects.filter(mandate=mandate)
                        visit_request_filter = FieldReqFilter(request.GET, queryset=visit_requests)
                        visit_req_count = visit_requests.count()
                        visit_requests = visit_request_filter.qs
                        if visit_requests:
                            for visit_req in visit_requests:
                                field_proforma = FieldProforma.objects.filter(field_request=visit_req).last()
                                visit_requests_list.append([cart_match, mandate_request, mandate, visit_req])
                                if field_proforma:
                                    field_invoice = FieldInvoice.objects.filter(field_proforma=field_proforma).last()
                                    visit = Field.objects.filter(proforma=field_proforma).last()
                                    field_proforma_list.append([cart_match, mandate_request, mandate, visit_req,
                                                                field_proforma])
                                    if field_invoice:
                                        field_invoice_list.append([cart_match, mandate_request, mandate, visit_req,
                                                                   field_proforma, field_invoice])
                                    if visit:
                                        visit_list.append([cart_match, mandate_request, mandate, visit_req, field_proforma,
                                                           visit])

    context = {
        'mine': mine,
        'mine_area': mine_area,
        'poly': polygon,
        'mineloc': mineloc,
        'claims_filter': claims_filter,
        'claims': claimpoly,
        'mandate_count': mandate_count,
        'visit_req_count': visit_req_count,
        'cart_match_count': cart_match_count,
        'visit_count': visit_count,
        'field_proforma_count': field_proforma_count,
        'visit_requests_list': visit_requests_list,
        'field_proforma_list': field_proforma_list,
        'visit_list': visit_list,
        'field_invoice_list': field_invoice_list,
        'field_invoice_count': field_invoice_count,
        'mandate_list': mandate_list,
        'mandate_request_list': mandate_request_list,
        'mandate_req_status': mandate_req_status,
        'mandate_request_count': mandate_request_count,
        'filter': cart_filter,
        'mineral_count': mineral_count,
        'ore_count': ore_count,
        'waste_count': waste_count,
        'mineral_production': mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'minerals': minerals,
        'mineral_set': mineral_set,
        'units_set': units_set,
        'ore': ore,
        'waste': waste,
        'works': works,
        'labour': labour,
        'plant': plant,
        'mobile': mobile,
        'reports': reports,
        'attachments': attachments,
        'works_filter': works_filter,
        'plant_filter': plant_filter,
        'mobile_filter': mobile_filter,
        'sample_points': sample_points,
        'alerts': alerts,
        'cancel': cancel,
    }
    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mandate_proforma_new(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate_request = MandateRequest.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')
    rates = Rates.objects. all()

    if request.method == 'POST':
        form = MandateProformaForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mandate_request_id = mandate_request.id
            record.date_created = Now()
            record = form.save(commit=False)

            if MandateProforma.objects.filter(mandate_request=mandate_request).exists():
                messages.info(request, 'Proforma already exists')
                return redirect('mandate_request_detail.html', pk=mandate_request.id)

            record.author = request.user
            record.save()

        return redirect('mandate_request_detail.html', pk=mandate_request.id)

    else:
        form = MandateProformaForm()

    context = {
        'form': form,
        'mandate_request': mandate_request,
        'rates': rates,
        'cancel': cancel,
    }
    return render(request, 'mandate_proforma_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def support_costs_new(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    field_request = FieldReq.objects.get(id=pk)
    rates = Rates.objects. all()
    cancel = request.META.get('HTTP_REFERER')
    costs = FieldSupCosts.objects.filter(field_request=field_request)
    cost_item = 0
    if field_request.service_req == 'True':
        if ServiceProvRequired.objects.filter(field_request=field_request):
            for service in ServiceProvRequired.objects.filter(field_request=field_request):
                if service.fieldreqwinqte_set.all():
                    if service.fieldreqwinqte_set.all().count == service.quantity:
                        pass
                else:
                    messages.info(request, 'Some Quotations are still outstanding')
                    return redirect(cancel)

    if request.method == 'POST':
        form = SupportCostForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.field_request_id = field_request.id
            record.final = record.cost
            record = form.save(commit=False)
            if FieldSupCosts.objects.filter(field_request_id=record.field_request.id, cost_type_id=record.cost_type.id).exists():
                cost_item = FieldCostList.objects.get(id=record.cost_type_id)
                messages.info(request,  str(cost_item) + ' cost already exist')
                form = SupportCostForm()
                context = {
                    'form': form,
                    'field_request': field_request,
                    'rates': rates,
                    'costs': costs,
                    'cancel': cancel,
                }
                return render(request, 'investor/support_costs_new.html', context)

            record.date_created = Now()
            record.save()

            form = SupportCostForm()
            context = {
                'form': form,
                'field_request': field_request,
                'rates': rates,
                'costs': costs,
                'cancel': cancel,
            }
            return render(request, 'investor/support_costs_new.html', context)

    else:
        form = SupportCostForm()

        context = {
            'form': form,
            'field_request': field_request,
            'rates': rates,
            'costs': costs,
            'cancel': cancel,
            'alerts': alerts,
        }
        return render(request, 'investor/support_costs_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_activity_create(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field_request = FieldReq.objects.get(id=pk)
    proforma = field_request.fieldproforma_set.all().last()
    cancel = request.META.get('HTTP_REFERER')
    activities = Field.objects.filter(proforma=proforma)

    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.proforma_id = proforma.id
            record = form.save(commit=False)
            if Field.objects.filter(subject=record.subject, proforma_id=record.proforma.id).exists():
                messages.info(request,  str(record.subject) + ' already exists')
                form = FieldForm()
                context = {
                    'form': form,
                    'field_request': field_request,
                    'cancel': cancel,
                    'activities': activities,
                }
                return render(request, 'investor/field_activity_create.html', context)

            record.date_created = Now()
            record.author = request.user
            record.save()

            form = FieldForm()
            context = {
                'form': form,
                'field_request': field_request,
                'cancel': cancel,
                'activities': activities,
            }
            return render(request, 'investor/field_activity_create.html', context)

    else:
        form = FieldForm()

        context = {
            'form': form,
            'field_request': field_request,
            'cancel': cancel,
            'alerts': alerts,
            'activities': activities,
        }
        return render(request, 'investor/field_activity_create.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_activity_edit(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field = Field.objects.get(id=pk)
    post = get_object_or_404(Field, pk=pk)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = FieldForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            if Field.objects.filter(subject=record.subject, proforma_id=record.proforma.id).exists():
                if record.subject != field.subject:
                    messages.info(request,  'Field with Subject: ' + " " + str(record.subject) + ' already exists')
                    return redirect(cancel)

            record.save()

            return redirect(cancel )

    else:
        form = FieldForm(instance=post)

        context = {
            'form': form,
            'field': field,
            'cancel': cancel,
            'alerts': alerts,
        }
        return render(request, 'investor/field_activity_edit.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_activity_attach_new(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    activity = Field.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = FieldAttachForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.activity_id = activity.id
            record = form.save(commit=False)
            if FieldAttachments.objects.filter(activity_id=record.activity_id, type=record.type, name=record.name).exists():
                messages.info(request, 'Attachment already exists')
                return redirect('field_activity_detail_attach.html', pk=activity.id)

            record.date_created = Now()
            record.author = request.user
            record.save()

            return redirect('field_activity_detail_attach.html', pk=activity.id)

    else:
        form = FieldAttachForm()

        context = {
            'form': form,
            'activity': activity,
            'cancel': cancel,
            'alerts': alerts,
        }
        return render(request, 'field_attach_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_field_activity_attach_new(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    activity = Field.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = FieldAttachForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.activity_id = activity.id
            record = form.save(commit=False)
            if FieldAttachments.objects.filter(activity_id=record.activity_id, type=record.type, name=record.name).exists():
                messages.info(request, 'Attachment already exists')
                return redirect(cancel)

            record.date_created = Now()
            record.author = request.user
            record.save()

            return redirect(cancel)

    else:
        form = FieldAttachForm()

        context = {
            'form': form,
            'activity': activity,
            'cancel': cancel,
            'alerts': alerts,
        }
        return render(request, 'services/proview/field/attach_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_field_activity_acquit(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    activity = Field.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = FieldAcquitForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.activity_id = activity.id
            record.author = request.user
            record.acquit = 'True'
            record = form.save(commit=False)
            if FieldAcquit.objects.filter(activity_id=record.activity_id, author=record.author).exists():
                messages.info(request, 'Task already acquitted by Author')
                return redirect('services/proview/field/detail_attach.html', pk=activity.id)

            record.date_created = Now()
            record.save()

            return redirect('services/proview/field/detail_attach.html', pk=activity.id)

    else:
        form = FieldAcquitForm()

        context = {
            'form': form,
            'activity': activity,
            'cancel': cancel,
            'alerts': alerts,
        }
        return render(request, 'services/proview/field/acquit.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_activity_acquit(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    activity = Field.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = FieldAcquitForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.activity_id = activity.id
            record.author = request.user
            record = form.save(commit=False)
            if FieldAcquit.objects.filter(activity_id=record.activity_id, author=record.author).exists():
                messages.info(request, 'Task already acquitted by Author')
                return redirect('field_activity_detail_attach.html', pk=activity.id)

            record.date_created = Now()
            record.save()

            return redirect('field_activity_detail_attach.html', pk=activity.id)

    else:
        form = FieldAcquitForm()

        context = {
            'form': form,
            'activity': activity,
            'cancel': cancel,
            'alerts': alerts,
        }
        return render(request, 'field_acquit.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_field_activity_create(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field_request = FieldReq.objects.get(id=pk)
    proforma = field_request.fieldproforma_set.all().last()
    cancel = request.META.get('HTTP_REFERER')
    activities = Field.objects.filter(proforma=proforma)

    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.proforma_id = proforma.id
            record = form.save(commit=False)
            if Field.objects.filter(subject=record.subject, proforma_id=record.proforma.id).exists():
                messages.info(request,  str(record.subject) + ' already exists')
                form = FieldForm()
                context = {
                    'form': form,
                    'field_request': field_request,
                    'cancel': cancel,
                    'activities': activities,
                }
                return render(request, 'investor/investview/field/add.html', context)

            record.date_created = Now()
            record.author = request.user
            record.save()

            form = FieldForm()
            context = {
                'form': form,
                'field_request': field_request,
                'cancel': cancel,
                'activities': activities,
            }
            return render(request, 'investor/investview/field/add.html', context)

    else:
        form = FieldForm()

        context = {
            'form': form,
            'field_request': field_request,
            'cancel': cancel,
            'alerts': alerts,
            'activities': activities,
        }
        return render(request, 'investor/investview/field/add.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_field_activity_edit(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field = Field.objects.get(id=pk)
    post = get_object_or_404(Field, pk=pk)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = FieldForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            if Field.objects.filter(subject=record.subject, proforma_id=record.proforma.id).exists():
                if record.subject != field.subject:
                    messages.info(request,  'Field with Subject: ' + " " + str(record.subject) + ' already exists')
                    return redirect(cancel)

            record.save()

            return redirect(cancel )

    else:
        form = FieldForm(instance=post)

        context = {
            'form': form,
            'field': field,
            'cancel': cancel,
            'alerts': alerts,
        }
        return render(request, 'investor/investview/field/edit.html', context)

@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_proforma_new(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field_request = FieldReq.objects.get(id=pk)
    post = get_object_or_404(FieldReq,pk=pk)
    cancel = request.META.get('HTTP_REFERER')
    rates = Rates.objects. all()
    support_items = field_request.fieldsupcosts_set.all()
    support_costs = 0
    winning_costs = 0
    if support_items:
        for item in support_items:
            support_costs += item.cost
    provider_items = field_request.serviceprovrequired_set.all()
    if provider_items:
        for prov_item in provider_items:
            win_quotes = prov_item.fieldreqwinqte_set.all()
            if win_quotes:
                for quote in win_quotes:
                    winning_costs += quote.quote.cost

    if request.method == 'POST':
        form = FieldProformaForm(request.POST)
        form1 = FieldReqStatForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            record.field_request_id = field_request.id
            record = form.save(commit=False)
            if FieldProforma.objects.filter(field_request_id=field_request.id).exists():
                messages.info('Proforma already exists')
                redirect(cancel)
            record.provider_costs = winning_costs
            record.support_costs = support_costs
            record.amount = (support_costs + winning_costs)*(1+(record.admin_premium.premium/100))
            record.date_created = Now()
            record.author = request.user
            record.save()

            if form1.is_valid:
                form1 = form1.save(commit=False)
                form1.status = 'Proforma'
                form1.save()

                return redirect('investor/field_request_detail.html', pk=field_request.id)

    else:
        form = FieldProformaForm()
        form1 = FieldReqStatForm(instance=post)

    context = {
        'form': form,
        'form1': form1,
        'field_request': field_request,
        'rates': rates,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'field_proforma_new.html', context)

@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_new(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field_request = FieldReq.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')
    services = ServiceProvRequired.objects.filter(field_request=field_request)
    proforma = field_request.fieldproforma_set.all().last()
    activities = proforma.field_set.all()
    providers = []
    winning_quotes = None
    if services:
        for service in services:
            winning_quotes = FieldReqWinQte.objects.filter(service_ref=service)
            if winning_quotes:
                for quote in winning_quotes:
                    providers.append(quote.provider)

    if request.method == 'POST':
        form = FieldForm(request.POST, providers=providers)
        if form.is_valid():
            record = form.save(commit=False)
            record.proforma_id = proforma.id
            record.cancel = cancel
            record = form.save(commit=False)
            if Field.objects.filter(proforma_id=proforma.id, task=record.task).exists():
                messages.info('Task already exists')
                redirect(cancel)
            record.date_created = Now()
            record.author = request.user
            record.save()

            return redirect('investor/field_request_detail.html', pk=field_request.id)

    else:
        form = FieldForm()

    context = {
        'form': form,
        'field_request': field_request,
        'activities': activities,
        'providers': providers,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'field_proforma_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mining_claim_new(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    if request.method == 'POST':
        form = NewClaimForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.date_created = Now()
            record = form.save(commit=False)

            if MiningClaim.objects.filter(reg_number=record.reg_number).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'mining_claim_new.html', {'form': form})

            record.author = request.user
            record.save()
            return redirect('mining_claim_list.html')

    else:
        form = NewClaimForm()

    context = {
        'form': form,
        'alerts': alerts,
    }
    return render(request, 'mining_claim_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mining_claim_edit(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    post = get_object_or_404(MiningClaim, id=pk)
    claim = MiningClaim.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = NewClaimForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)

            if MiningClaim.objects.filter(reg_number=record.reg_number).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'mining_claim_new.html', {'form': form})
            record.save()
            return redirect('mining_claim_detail.html', pk=pk)

    else:
        form = NewClaimForm(instance=post)

    context = {
        'form': form,
        'claim': claim,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'mining_claim_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def attach_to_mine(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    claim = MiningClaim.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = AttachToMineForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.claim_id = pk
            record.date_created = Now()
            record.author = request.user
            record.save()
            return redirect('mining_claim_detail.html', pk=pk)

    else:
        form = AttachToMineForm()

    context = {
        'form': form,
        'claim': claim,
        'cancel': cancel,
        'alerts':alerts,
    }
    return render(request, 'attach_to_mine.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mining_claim_detail(request, pk, template):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    claim = MiningClaim.objects.get(id=pk)
    mineloc = None
    poly = None
    if claim.miningclaimpolygon_set.all():
        poly = claim.miningclaimpolygon_set.all().last()
    if MiningClaimLocation.objects.filter(name_id=pk):
        mineloc = MiningClaimLocation.objects.filter(name_id=pk).last()
    beacons = Beacon.objects.filter(mining_claim=claim)
    beacon_count = len(beacons)
    certificate = claim.claimregcert_set.all().last()


    context = {
        'claim': claim,
        'beacons': beacons,
        'beacon_count': beacon_count,
        'certificate': certificate,
        'alerts': alerts,
        'poly': poly,
        'mineloc': mineloc,
        'cancel': cancel,
    }
    return render(request, template, context)


def geo_jason(request, queryset, serialiser):
    return


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mining_claim_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    claims = MiningClaim.objects.all()
    claims_filter = ClaimsFilter(request.GET, queryset=claims)
    claims = claims_filter.qs
    records = claims

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    location_list = []
    marker = None
    for claim in claims:
        if MiningClaimLocation.objects.filter(name_id=claim.id).last():
            marker = MiningClaimLocation.objects.filter(name_id=claim.id).last()
            location_list.append(marker)

    context = {
        'filter': claims_filter,
        'page_obj': page_obj,
        'alerts': alerts,
        'locations': location_list,
    }
    return render(request, 'mining_claim_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mines = Mine.objects.all()
    mine_filter = MineFilter(request.GET, queryset=mines)
    mines = mine_filter.qs
    records = mines

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    location_list = []
    marker = None
    for mine in mines:
        if MineLocation.objects.filter(name_id=mine.id).last():
            marker = MineLocation.objects.filter(name_id=mine.id).last()
            location_list.append(marker)

    context = {
        'filter': mine_filter,
        'alerts': alerts,
        'locations': location_list,
        'page_obj': page_obj,
    }
    return render(request, 'mine_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mineview_archive(request, template):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    letters = None
    agreements = None
    receipts = None
    others = None
    letters_filter = None
    agreements_filter = None
    receipts_filter = None
    others_filter = None
    records = None
    records1 = None
    records2 = None
    records3 = None
    page_obj = None
    page_obj1 = None
    page_obj2 = None
    page_obj3 = None
    if MineLetters.objects.filter(player=player):
        letters = player.mineletters_set.all()
        letters_filter = MineviewArchiveLetterFilter(request.GET, queryset=letters, player=player)
        records = letters_filter.qs
        paginator = Paginator(records, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    if MineAgreements.objects.filter(player=player):
        agreements = player.mineagreements_set.all()
        agreements_filter = MineviewArchiveAgreementFilter(request.GET, queryset=agreements)
        records1 = agreements_filter.qs
        paginator1 = Paginator(records1, 15)
        page_number1 = request.GET.get('page')
        page_obj1 = paginator1.get_page(page_number1)
    if MineReceipts.objects.filter(player=player):
        receipts = player.minereceipts_set.all()
        receipts_filter = MineviewArchiveReceiptFilter(request.GET, queryset=receipts)
        records2 = receipts_filter.qs
        paginator2 = Paginator(records2, 15)
        page_number2 = request.GET.get('page')
        page_obj2 = paginator2.get_page(page_number2)
    if OtherDocs.objects.filter(player=player):
        others = player.otherdocs_set.all()
        others_filter = MineviewArchiveOtherFilter(request.GET, queryset=others)
        records3 = others_filter.qs
        paginator3 = Paginator(records3, 15)
        page_number3 = request.GET.get('page')
        page_obj3 = paginator3.get_page(page_number3)

    context = {
        'letters_filter': letters_filter,
        'agreements_filter': agreements_filter,
        'receipts_filter': receipts_filter,
        'others_filter': others_filter,
        'page_obj': page_obj,
        'page_obj1': page_obj1,
        'page_obj2': page_obj2,
        'page_obj3': page_obj3,
        'alerts': alerts,
    }
    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_employee_new(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(pk=pk)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = MineEmployeeForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            record.date_created = Now()
            record = form.save(commit=False)

            if Mine.objects.filter(employee=record.employee, job=record.job, post=record.post).exists():
                messages.info(request, 'Record already exists')
                return render(request, 'mining_employee_new.html', {'form': form})

            record.author = request.user
            record.save()
            return redirect('mine_detail.html', pk=record.mine.id)

    else:
        form = MineEmployeeForm()

    context = {
        'form': form,
        'mine': mine,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'mining_employee_new.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_employee_edit(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    post = get_object_or_404(MineEmployees, pk=pk)
    cancel = request.META.get('HTTP_REFERER')
    employee = MineEmployees.objects.get(id=pk)

    if request.method == 'POST':
        form = MineEmployeeEditForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)

            if MiningClaim.objects.filter(reg_number=record.reg_number).exists():
                messages.info(request, 'Entity already exists')
                return render(request, 'mining_claim_new.html', {'form': form})
            record.save()
            return redirect('mine_detail.html', pk=pk)

    else:
        form = MineEmployeeEditForm()

    context = {
        'form': form,
        'employee': employee,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'mine_employee_edit.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_employee_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = MineEmployees.objects.all()
    filter = MineEmployeesFilter(request.GET, queryset=records)

    context = {
        'filter': filter,
        'alerts': alerts,
    }
    return render(request, 'mine_employee_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_report_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = MineReports.objects.all()
    filter = MineReportFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'mine_report_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_report_detail(request, pk):
    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    report = MineReports.objects.get(id=pk)

    context = {
        'report': report,
        'alerts': alerts,
    }
    return render(request, 'mine_report_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mineview_mine_report_detail(request, pk):
    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    report = MineReports.objects.get(id=pk)

    context = {
        'report': report,
        'alerts': alerts,
    }
    return render(request, 'mineowner/report_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_mine_report_detail(request, pk):
    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    report = MineReports.objects.get(id=pk)

    context = {
        'report': report,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/mine/report_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_mine_report_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    report = MineReports.objects.get(id=pk)

    context = {
        'report': report,
        'alerts': alerts,
    }
    return render(request, 'services/proview/mine/report_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_certificate_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = MineCertificates.objects.all()
    filter = MineCertificateFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'mine_certificate_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def plant_pictures(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)

    plant_pics = PlantImages.objects.filter(plant_id=pk)
    item = MinePlant.objects.get(id=pk)
    services = EquipmentService.objects.filter(fixed_plant_id=pk)
    distances = EquipmentMileage.objects.filter(fixed_plant_id=pk)
    records = plant_pics

    paginator = Paginator(records, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    paginator1 = Paginator(services, 8)
    page_number1 = request.GET.get('page')
    service = paginator1.get_page(page_number1)

    paginator2 = Paginator(distances, 8)
    page_number2 = request.GET.get('page')
    mileage = paginator2.get_page(page_number2)

    context = {
        'alerts': alerts,
        'page_obj': page_obj,
        'item': item,
        'service':service,
        'mileage': mileage,
    }
    return render(request, 'pictures.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def yellow_pictures(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)

    plant_pics = YellowImages.objects.filter(plant_id=pk)
    item = MineYellowPlant.objects.get(id=pk)
    services = EquipmentService.objects.filter(mobile_plant_id=pk)
    distances = EquipmentMileage.objects.filter(mobile_plant_id=pk)
    records = plant_pics

    paginator = Paginator(records, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    paginator1 = Paginator(services, 8)
    page_number1 = request.GET.get('page')
    service = paginator1.get_page(page_number1)

    paginator2 = Paginator(distances, 8)
    page_number2 = request.GET.get('page')
    mileage = paginator2.get_page(page_number2)

    context = {
        'alerts': alerts,
        'page_obj': page_obj,
        'item': item,
        'service':service,
        'mileage': mileage,
    }
    return render(request, 'yellow_pictures.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def works_pictures(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)

    plant_pics = WorksImages.objects.filter(plant_id=pk)
    item = MineWorks.objects.get(id=pk)
    work_devs = WorksDev.objects.filter(works_id=pk)

    records = plant_pics
    paginator = Paginator(records, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    paginator3 = Paginator(work_devs, 12)
    page_number3 = request.GET.get('page')
    devs = paginator3.get_page(page_number3)

    context = {
        'alerts': alerts,
        'page_obj': page_obj,
        'item': item,
        'devs': devs,
    }
    return render(request, 'works_pictures.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_picture_plant(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    item = MinePlant.objects.get(id=pk)
    image_count = PlantImages.objects.filter(plant_id=pk).count()

    if request.method == 'POST':
        form = PlantImageForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.plant_id = item.id
            record.date_created = Now()
            record.save()

        return redirect(cancel)

    form = PlantImageForm()

    context = {
        'alerts': alerts,
        'form': form,
        'item': item,
        'image_count': image_count,
        'cancel': cancel,
    }
    return render(request, 'add_picture.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_picture_mobile(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    item = MineYellowPlant.objects.get(id=pk)
    image_count = YellowImages.objects.filter(plant_id=pk).count()

    if request.method == 'POST':
        form = YellowImageForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.plant_id = item.id
            record.date_created = Now()
            record.save()

        return redirect(cancel)

    form = YellowImageForm()

    context = {
        'alerts': alerts,
        'form': form,
        'item': item,
        'image_count': image_count,
        'cancel': cancel,
    }
    return render(request, 'add_picture.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_picture_works(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    item = MineWorks.objects.get(id=pk)
    image_count = WorksImages.objects.filter(plant_id=pk).count()

    if request.method == 'POST':
        form = WorksImageForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.plant_id = item.id
            record.date_created = Now()
            record.save()

        return redirect(cancel)

    form = WorksImageForm()

    context = {
        'alerts': alerts,
        'form': form,
        'item': item,
        'image_count': image_count,
        'cancel': cancel,
    }
    return render(request, 'add_picture.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_service(request, pk, source):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    item = None
    if request.method == 'POST':
        form = PlantServiceForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            if source == 'plant':
                item = MinePlant.objects.get(id=pk)
                record.fixed_plant_id = pk
            else:
                item = MineYellowPlant.objects.get(id=pk)
                record.mobile_plant_id = pk
            record.date_created = Now()
            record.author = request.user
            record.save()

        return redirect(cancel)
    else:
        form = PlantServiceForm()

    context = {
        'alerts': alerts,
        'form': form,
        'item': item,
        'source': source,
        'cancel': cancel,
    }
    return render(request, 'add_service.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def plant_usage(request, pk, source):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    item = None
    if request.method == 'POST':
        form = PlantUsageForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            if source == 'plant':
                item = MinePlant.objects.get(id=pk)
                record.fixed_plant_id = pk
            else:
                item = MineYellowPlant.objects.get(id=pk)
                record.mobile_plant_id = pk
            record.date_created = Now()
            record.author = request.user
            record.save()

        return redirect(cancel)
    else:
        form = PlantUsageForm()

    context = {
        'alerts': alerts,
        'form': form,
        'item': item,
        'source': source,
        'cancel': cancel,
    }
    return render(request, 'add_usage.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_works_activity(request, pk, source):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    item = MineWorks.objects.get(id=pk)
    if request.method == 'POST':
        form = WorksDevForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.works_id = pk
            record.date_created = Now()
            record.author = request.user
            record.save()

        return redirect(cancel)
    else:
        form = WorksDevForm()

    context = {
        'alerts': alerts,
        'form': form,
        'item': item,
        'source': source,
        'cancel': cancel,
    }
    return render(request, 'work_devs.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_certificate_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    certificate = MineCertificates.objects.get(id=pk)

    context = {
        'certificate': certificate,
        'alerts': alerts,
    }
    return render(request, 'mine_certificate_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def view_image_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    certificate = MineCertificates.objects.get(id=pk)

    context = {
        'certificate': certificate,
        'alerts': alerts,
    }
    return render(request, 'mine_certificate_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def claim_reg_cert_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    claim_reg = ClaimRegCert.objects.get(id=pk)

    context = {
        'certificate': claim_reg,
        'alerts': alerts,
    }
    return render(request, 'claim_reg_cert_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_field_attach_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    attachment = FieldAttachments.objects.get(id=pk)

    context = {
        'attachment': attachment,
        'alerts': alerts,
    }
    return render(request, 'services/proview/field/attach_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mineview_claim_reg_cert_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    claim_reg = ClaimRegCert.objects.get(id=pk)

    context = {
        'certificate': claim_reg,
        'alerts': alerts,
    }
    return render(request, 'mine_owner/claim_reg_cert_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def claim_reg_cert_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = ClaimRegCert.objects.all()
    filter = ClaimRegFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'claim_reg_cert_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_activity_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = Field.objects.all()
    filter = FieldFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'investor/field_activity_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_request_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = FieldReq.objects.all()
    filter = FieldReqFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'investor/field_request_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_proforma_ready(request):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field_requests = FieldReq.objects.filter(status='Service Choice')
    filter = FieldReqReadyFilter(request.GET, queryset=field_requests)
    requests_ready = []
    if field_requests:
        for field_request in field_requests:
            services = field_request.serviceprovrequired_set.all()
            if services:
                for service in services:
                    if service.status == 'Completed':
                        if FieldSupCosts.objects.filter(field_request=field_request):
                            if not FieldProforma.objects.filter(field_request=field_request):
                                requests_ready.append(field_request)

    context = {
        'filter': filter,
        'alerts': alerts,
        'requests_ready': requests_ready,
    }
    return render(request, 'field_proforma_ready.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_costing_list(request):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field_requests = FieldReq.objects.filter(status='Service Choice')
    filter = FieldReqReadyFilter(request.GET, queryset=field_requests)
    wins_count = []
    records = wins_count

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if field_requests:
        for field_request in field_requests:
            services = field_request.serviceprovrequired_set.all()
            if services:
                for service in services:
                    wins = FieldReqWinQte.objects.filter(service_ref=service)
                    if wins:
                        wins_count.append(field_request)
                        if wins.count != service.quantity:
                            pass
                        else:
                            wins_count.append(field_request)

    context = {
        'filter': filter,
        'page_obj': page_obj,
        'alerts': alerts,
        'wins_count': wins_count,
    }
    return render(request, 'field_costing_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_proforma_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = FieldProforma.objects.all()
    filter = FieldProformaFilter(request.GET, queryset=records)

    context = {
        'filter': filter,
        'alerts': alerts,
    }
    return render(request, 'field_proforma_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mandate_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = Mandate.objects.all()
    filter = MandateFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'investor/mandate_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mandate_request_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = MandateRequest.objects.all()
    filter = MandateRequestFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'investor/mandate_request_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mandate_proforma_ready(request):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    mandate_requests = MandateRequest.objects.all()
    mandate_request_list = []
    filter = MandateRequestReadyFilter(request.GET, queryset=mandate_requests)
    for mandate_request in mandate_requests:
        if mandate_request.mandateproforma_set.all():
            pass
        else:
            if mandate_request.minemandaterequest_set.all().last().status == 'Pending':
                mandate_request_list.append(mandate_request)

    context = {
        'filter': filter,
        'alerts': alerts,
        'mandate_request_list': mandate_request_list
    }
    return render(request, 'mandate_proforma_ready.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def cart_match_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = CartMineMatch.objects.all()
    filter = CartMineMatchFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'investor/cart_match_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def cart_mine_match_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = CartMineMatch.objects.all()
    filter = CartRequestFilter(request.GET, queryset=records)

    context = {
        'filter': filter,
        'alerts': alerts,
    }
    return render(request, 'investor/cart_mine_match_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def cart_request_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = CartRequest.objects.all()
    filter = CartRequestFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'investor/cart_request_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_cart_request_list(request):

    player = request.user.playeruserrelation_set.all().last().player
    alerts = Alerts.objects.filter(player=player)
    investor = player.investor_set.all().last()
    records = CartRequest.objects.filter(investor_id=investor.id)
    filter = CartRequestFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'investor/investview/cart/list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investor_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = Investor.objects.all()
    filter = InvestorFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'investor/list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def receipt_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = Receipt.objects.all()
    filter = ReceiptFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'receipt_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_fieldreq_detail(request, pk):

    field_request = FieldReq.objects.get(id=pk)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    provider = player.serviceprov_set.all().last()
    activities = []
    attachments = []
    actions = None
    service_ref = ServiceProvRequired.objects.filter(field_request=field_request, provider_role=provider.rating).last()
    quote = FieldProviderQuote.objects.filter(service_ref=service_ref).last()
    if field_request.fieldproforma_set.all():
        actions = field_request.fieldproforma_set.all().last().field_set.all()
        if actions:
            for activity in actions:
                if activity.fiedlproviderrelation_set.filter(provider=provider):
                    activities.append(activity)
                    if activity.fieldattachments_set.all():
                        for attach in activity.fieldattachments_set.all():
                            if attach.author == request.user:
                                attachments.append(attach)

    context = {
        'field_request': field_request,
        'alerts': alerts,
        'activities': activities,
        'attachments': attachments,
        'provider': provider,
        'quote': quote,
    }
    return render(request, 'services/proview/fieldreq/claims.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_fieldreq_quote(request, pk):

    field_request = FieldReq.objects.get(pk=pk)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    provider = player.serviceprov_set.all().last()
    activities = []
    attachments = []
    actions = None
    service_ref = ServiceProvRequired.objects.filter(field_request=field_request, provider_role=provider.rating).last()
    quote = FieldProviderQuote.objects.filter(service_ref=service_ref).last()
    if field_request.fieldproforma_set.all():
        actions = field_request.fieldproforma_set.all().last().field_set.all()
        if actions:
            for activity in actions:
                if activity.fiedlproviderrelation_set.filter(provider=provider):
                    activities.append(activity)
                    if activity.fieldattachments_set.all():
                        for attach in activity.fieldattachments_set.all():
                            if attach.author == request.user:
                                attachments.append(attach)


    context = {
        'field_request': field_request,
        'alerts': alerts,
        'activities': activities,
        'attachments': attachments,
        'provider': provider,
        'quote': quote,
    }
    return render(request, 'services/proview/fieldreq/quote.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_fieldreq_attach(request, pk):

    field_request = FieldReq.objects.get(pk=pk)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    provider = player.serviceprov_set.all().last()
    activities = []
    attachments = []
    actions = None
    service_ref = ServiceProvRequired.objects.filter(field_request=field_request, provider_role=provider.rating).last()
    quote = FieldProviderQuote.objects.filter(service_ref=service_ref).last()
    if field_request.fieldproforma_set.all():
        actions = field_request.fieldproforma_set.all().last().field_set.all()
        if actions:
            for activity in actions:
                if activity.fiedlproviderrelation_set.filter(provider=provider):
                    activities.append(activity)
                    if activity.fieldattachments_set.all():
                        for attach in activity.fieldattachments_set.all():
                            if attach.author == request.user:
                                attachments.append(attach)


    context = {
        'field_request': field_request,
        'alerts': alerts,
        'activities': activities,
        'attachments': attachments,
        'provider': provider,
        'quote': quote,
    }
    return render(request, 'services/proview/fieldreq/attach.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def quote_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    quote = FieldProviderQuote.objects.get(id=pk)

    context = {
        'quote': quote,
        'alerts': alerts,
    }
    return render(request, 'quote_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def provider_fieldreq_list(request):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    provider = online.serviceprov_set.all().last()
    service_list = []
    location_list = []
    mine_list = []
    records = 0
    mine = None
    if ServiceProvRequired.objects.all():
        records = ServiceProvRequired.objects.filter(provider_role_id=provider.rating.id)
        filter = ServiceReqFilter(request.GET, queryset=records)
        records = filter.qs
        if records != 0:
            for record in records:
                if record.status != 'Completed':
                    if FieldProviderQuote.objects.filter(service_ref=record, provider=provider):
                        pass
                    else:
                        service_list.append(record)
    x = 0
    for item in service_list:
        mine = item.service_ref.field_request.mandate.mandate_request.mine
        marker = MineLocation.objects.filter(name_id=mine.id).last()
        if mine not in mine_list:
            mine_list.append(mine)
            location_list.append([marker, [item,]])
        else:
            x = mine_list.index(mine)
            location_list[x][1].append(item)

    context = {
        'filter': filter,
        'alerts': alerts,
        'service_list': service_list,
        'locations': location_list,
    }
    return render(request, 'services/proview/fieldreq/list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def provider_fieldreq_quoted_list(request):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    provider = online.serviceprov_set.all().last()
    service_list = []
    location_list = []
    mine_list = []
    records = None
    mine = None
    records = service_list

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if ServiceProvRequired.objects.all():
        records = FieldProviderQuote.objects.filter(provider=provider)
        filter = ProviderQuoteFilter(request.GET, queryset=records)
        records = filter.qs
        if records:
            for record in records:
                service_list.append(record.service_ref)

    x = 0
    for item in service_list:
        mine = item.field_request.mandate.mandate_request.mine
        marker = MineLocation.objects.filter(name_id=mine.id).last()
        if mine not in mine_list:
            mine_list.append(mine)
            location_list.append([marker, [item,]])
        else:
            x = mine_list.index(mine)
            location_list[x][1].append(item)

    map_centre = None
    if location_list.count != 0:
        map_centre = location_list[0][0].lat_long

    context = {
        'filter': filter,
        'alerts': alerts,
        'service_list': service_list,
        'page_obj': page_obj,
        'locations': location_list,
        'map_centre': map_centre,
    }
    return render(request, 'services/proview/fieldreq/quoted_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def invoice_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = Invoice.objects.all()
    filter = InvoiceFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'invoice_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mandate_request_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate_request = MandateRequest.objects.get(id=pk)
    mine = mandate_request.mine
    mineloc = None
    polygon = None
    if MineLocation.objects.filter(name_id=mine.id):
        mineloc = MineLocation.objects.filter(name_id=mine.id).last()
    if mine.minepolygon_set.all():
        polygon = mine.minepolygon_set.all().last()
    cart_match = mandate_request.cart_mine_match
    cart_request = cart_match.cart_request
    mines_matched = CartMineRelation.objects.filter(cart=cart_match)

    context = {
        'cart_request': cart_request,
        'cart_match': cart_match,
        'mandate_request': mandate_request,
        'mines_matched': mines_matched,
        'poly': polygon,
        'mineloc': mineloc,
        'alerts': alerts,
    }
    return render(request, 'investor/mandate_request_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mandate_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cart_request = CartRequest.objects.get(id=pk)
    cart_match = CartMineMatch.objects.filter(cart_request=cart_request).last()
    mines_matched = CartMineRelation.objects.filter(cart_request=cart_request)
    mineloc = []
    polygon = None
    if mines_matched:
        for mine in mines_matched:
            loc = MineLocation.objects.filter(name_id=mine.id).last()
            mineloc.append(loc)

        mineloc = mineloc[0]
        polygon = mineloc[0].name.minepolygon_set.all().last()
    mandate_requests = MandateRequest.objects.filter(cart_match=cart_match)
    mandate_request_filter = MandateRequestFilter(request.GET, queryset=mandate_requests)
    mandate_requests = mandate_request_filter.qs
    mandate_request_count =mandate_requests.count

    context = {
        'cart_request': cart_request,
        'cart_match': cart_match,
        'mines_matched': mines_matched,
        'mandate_request_filter': mandate_request_filter,
        'mandate_request_count': mandate_request_count,
        'poly': polygon,
        'mineloc': mineloc,
        'alerts': alerts,
    }
    return render(request, 'investor/mandate_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_cart_match(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    cart_request = CartRequest.objects.get(id=pk)

    if request.method == 'POST':
        form = CartMatchForm(request.POST)
        form1 = InvestorMineForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.cart_request_id = cart_request.id
            record.date_created = Now()
            record = form.save(commit=False)

            if CartMineMatch.objects.filter(cart_request_id=record.cart_request.id).exists():
                messages.info(request, 'Match already exists ')
                context = {
                        'cart_request': cart_request,
                        'form': form,
                        'form1': form1,
                        'cancel': cancel,
                    }
                return render(request, 'investor/investview_cart_match.html', context)

            record.author = request.user
            record.save()

            for cart in record.mines.all():
                if form1.is_valid():
                    form1 = form.save(commit=False)
                    form1.mine_id = cart
                    form1.investor_id = cart_request.investor.id
                    form1.valid = record.valid
                    form1.date_created = Now()
                    form1 = form1.save()

            return redirect('investor/cart_request_detail.html', pk=cart_request.id)

    form = CartMatchForm()
    form1 = InvestorMineForm()
    context = {
        'cart_request': cart_request,
        'form': form,
        'form1': form1,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'investor/investview_cart_match.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_request_mandates(request, pk):

    cancel = request.META.get('HTTP_REFERER')
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cart_mine = CartMineRelation.objects.filter(mine_id=pk).last()
    mine = Mine.objects.get(id=pk)
    cart_mine_match = cart_mine.cart
    cart_request = cart_mine_match.cart_request
    if cart_request.valid <= timezone.now():
        messages.info(request, str(cart_request) + ' expired')
        return redirect(cancel)

    if request.method == 'POST':
        form = MandateRequestForm(request.POST)
        form1 = InvestorMineForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            record.cart_mine_match_id = cart_mine_match.id
            record = form.save(commit=False)
            mandate_req_last = MandateRequest.objects.filter(cart_mine_match_id=cart_mine_match.id).last()
            if mandate_req_last:
                if mandate_req_last.exists() and (mandate_req_last.period + datetime.timedelta(days=mandate_req_last.duration))<= record.period:
                    messages.info(request, str(cart_mine_match.mine) + ' Mandate already exists')
                    context = {
                            'mine': mine,
                            'cart_request': cart_request,
                            'form': form,
                            'form1': form1,
                            'cancel': cancel,
                        }
                    return render(request, 'investor/investview_request_mandates.html', context)

            record.date_created = Now()
            record.author = request.user
            record.save()

            if form1.is_valid():
                form1 = form1.save(commit=False)
                form1.mine_id = mine.id
                form1.investor_id = cart_request.investor.id
                form1.status = 'Mandate-Request'
                form1.date_created = Now()
                form1.save()

                return redirect('investor/investview/cart/mandate_request.html', pk=cart_request.id)

    form = MandateRequestForm()
    form1 = InvestorMineForm()
    context = {
        'mine': mine,
        'cart_request': cart_request,
        'form': form,
        'form1': form1,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'investor/investview_request_mandates.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_cart_detail(request, pk, template):

    cart_request = CartRequest.objects.get(id=pk)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cart_match = CartMineMatch.objects.filter(cart_request_id=pk).last()
    mines_matched = cart_match.mines.all()
    mines_available = []
    mines_remaining = []
    polygons = []
    min_locs = []
    for min in mines_matched:
        mineloc = MineLocation.objects.filter(name=min).last()
        pol = MinePolygon.objects.filter(name=min).last()
        polygons.append(pol)
        min_locs.append(mineloc)
    if mines_matched:
        for match in mines_matched:
            if MandateRequest.objects.filter(cart_mine_match=CartMineRelation.objects.filter(mine=match).last().cart):
                pass
            else:
                if cart_match.valid < datetime.now().date():
                    pass
                else:
                    mines_available.append(match)

    mandate_requests = MandateRequest.objects.filter(cart_mine_match=cart_match)
    mandate_request_filter = MandateRequestFilter(request.GET, queryset=mandate_requests)
    mandate_requests = mandate_request_filter.qs
    mandate_request_count =mandate_requests.count
    mandate_list = []
    field_request_list = []
    activities = []
    for mandate_request in mandate_requests:
        mandate = mandate_request.mandate_set.all().last()
        if mandate:
            mandate_list.append(mandate)
            field_requests = mandate.fieldreq_set.all()
            if field_requests:
                for field_request in field_requests:
                    field_request_list.append(field_request)
                    proforma = field_request.fieldproforma_set.all().last()
                    if proforma:
                        activity = proforma.field_set.all().last()
                        if activity:
                            activities.append([activity, field_request])


    location_list = []
    for mine in mines_matched:
        if MineLocation.objects.filter(name_id=mine.id).last():
            marker = MineLocation.objects.filter(name_id=mine.id).last()
            location_list.append(marker)

    context = {
        'cart_request': cart_request,
        'cart_match': cart_match,
        'mines_matched': mines_matched,
        'min_locs': min_locs,
        'polygons': polygons,
        'mandate_request_filter': mandate_request_filter,
        'mandate_request_count': mandate_request_count,
        'mandate_requests': mandate_requests,
        'mandate_list': mandate_list,
        'activities': activities,
        'field_request_list': field_request_list,
        'mines_available': mines_available,
        'alerts': alerts,
        'locations': location_list,
    }
    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def cart_request_detail(request, pk, template):

    cart_request = CartRequest.objects.get(id=pk)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cart_match = CartMineMatch.objects.filter(cart_request_id=pk).last()
    mines_matched = cart_match.mines.all()
    mines_available = []
    mines_remaining = []
    polygons = []
    min_locs = []
    for min in mines_matched:
        mineloc = MineLocation.objects.filter(name=min).last()
        pol = MinePolygon.objects.filter(name=min).last()
        polygons.append(pol)
        min_locs.append(mineloc)
    cart_req_mandate = 'investor/cart_req_mandate.html'
    if mines_matched:
        for match in mines_matched:

            if MandateRequest.objects.filter(cart_mine_match=CartMineRelation.objects.filter(mine=match).last().cart):
                pass
            else:
                if cart_match.valid < datetime.now().date():
                    pass
                else:
                    mines_available.append(match)

    mandate_requests = MandateRequest.objects.filter(cart_mine_match=cart_match)
    mandate_request_filter = MandateRequestFilter(request.GET, queryset=mandate_requests)
    mandate_requests = mandate_request_filter.qs
    mandate_request_count =mandate_requests.count
    mandate_list = []
    mandate_count = len(mandate_list)
    field_request_list = []
    field_request_count = field_request_list.count
    activities = []
    for mandate_request in mandate_requests:
        mandates = mandate_request.mandate_set.all()
        if mandates:
            for mandate in mandates:
                mandate_list.append(mandate)
                field_requests = mandate.fieldreq_set.all()
                if field_requests:
                    for field_request in field_requests:
                        field_request_list.append(field_request)
                        proforma = field_request.fieldproforma_set.all().last()
                        if proforma:
                            activity = proforma.field_set.all().last()
                            if activity:
                                activities.append([activity, field_request])

    context = {
        'cart_request': cart_request,
        'cart_match': cart_match,
        'mines_matched': mines_matched,
        'min_locs': min_locs,
        'polygons': polygons,
        'mandate_request_filter': mandate_request_filter,
        'mandate_request_count': mandate_request_count,
        'mandate_requests': mandate_requests,
        'mandate_list': mandate_list,
        'mandate_count': mandate_count,
        'field_request_count': field_request_count,
        'field_request_list': field_request_list,
        'activities': activities,
        'mines_available': mines_available,
        'alerts': alerts,
        'cart_req_mandate': cart_req_mandate,
    }

    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_field_req_act_detail(request, pk):

    field_request = FieldReq.objects.get(id=pk)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    services = field_request.serviceprovrequired_set.all()
    quotes = []
    quote_count = len(quotes)
    quotations = None
    provider_filter = None
    if services:
        for service in services:
            quotations = service.fieldproviderquote_set.all()
            provider_filter = FieldProviderQuoteFilter(request.GET, queryset=quotations)
            if quotations:
                for quote in quotations:
                    quotes.append(quote)
    activity_count = 0
    activities = []
    actions = None
    proforma = field_request.fieldproforma_set.all().last()
    if proforma:
        actions = proforma.field_set.all()
        activity_count = len(actions)
        for activity in actions:
            activities.append([activity, proforma])

    context = {
        'quotes': quotes,
        'field_request': field_request,
        'activities': activities,
        'activity_count': activity_count,
        'quote_count': quote_count,
        'provider_filter': provider_filter,
        'services': services,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/fieldreq/field_activity.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_field_req_quote_detail(request, pk):

    field_request = FieldReq.objects.get(id=pk)
    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    services = ServiceProvRequired.objects.filter(field_request_id=field_request.id)
    quotes = []
    quote_count = len(quotes)
    quotations = FieldProviderQuote.objects.all()
    provider_filter = FieldProviderQuoteFilter(request.GET, queryset=quotations)
    quotations = provider_filter.qs
    if services:
        for service in services:
            if quotations:
                quote_items = quotations.filter(service_ref_id=service.id)
                for quote in quote_items:
                    quotes.append(quote)
    activity_count = 0
    activities = []
    actions = None
    proforma = field_request.fieldproforma_set.all().last()
    if proforma:
        actions = proforma.field_set.all()
        activity_count = len(actions)
        for activity in actions:
            activities.append([activity, proforma])

    context = {
        'quotes': quotes,
        'field_request': field_request,
        'activities': activities,
        'activity_count': activity_count,
        'quote_count': quote_count,
        'provider_filter': provider_filter,
        'services': services,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/fieldreq/field_quote.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_field_quotation(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    quote = FieldProviderQuote.objects.get(id=pk)
    win_status:bool = False
    win_list = []
    wins = quote.service_ref.fieldreqwinqte_set.all()
    for win in wins:
        win_list.append(win.quote)
    if quote is win_list:
        win_status:bool = True

    context = {
        'quote': quote,
        'win_status': win_status,
        'alerts': alerts,
    }

    return render(request, 'investor/investview/quote_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_quote_accept_confirm(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    quote = FieldProviderQuote.objects.get(id=pk)
    post = get_object_or_404(FieldReq, pk=quote.service_ref.field_request.id)
    post1 = get_object_or_404(ServiceProvRequired, pk=quote.service_ref.id)
    post2 = get_object_or_404(FieldProviderQuote, pk=quote.id)
    if request.method == 'POST':
        form = QuoteAcceptForm(request.POST)
        form1 = FieldReqStatForm(request.POST, instance=post)
        form2 = FieldServStatForm(request.POST, instance=post1)
        form3 = FieldProviderQuoteCounterForm(request.POST, instance=post2)
        if form.is_valid():
            record = form.save(commit=False)
            record.service_ref_id = quote.service_ref.id
            record.quote_id = quote.id
            record.date_created = Now()
            record.author = request.user
            record.save()

            if form1.is_valid():
                form1 = form1.save(commit=False)
                form1.status = 'Service Choice'
                form1.save()

                if form2.is_valid():
                    form2 = form2.save(commit=False)
                    if quote.service_ref.quantity == quote.service_ref.fieldreqwinqte_set.all().count:
                        form2.status = 'Completed'
                    form2.save()

                    if form3.is_valid():
                        form3 = form3.save(commit=False)
                        form3.status = 'Success'
                        form3.save()

                        return redirect('investor/investview/fieldreq/quote.html', pk=quote.id)

    form = QuoteAcceptForm()
    form1 = FieldReqStatForm(instance=post)
    form2 = FieldServStatForm(instance=post1)
    form3 = FieldProviderQuoteCounterForm(instance=post2)
    context = {
        'quote': quote,
        'form':form,
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'alerts': alerts,
    }

    return render(request, 'investor/investview/quote_accept_confirm.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_field_proforma_pay(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    proforma = FieldProforma.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')
    post = get_object_or_404(Player, pk=online.id)
    if post.trxn_balance < proforma.amount:
        messages.info(request, '$ ' + str(post.trxn_balance) + ' - In-sufficient balance to settle payment')
        return redirect(cancel)
    post1 = get_object_or_404(FieldReq, pk=proforma.field_request.id)
    post3 = get_object_or_404(Player, pk=1)
    post4 = get_object_or_404(FieldProforma, pk=proforma.id)
    post2 = None
    invoice = None
    if request.method == 'POST':
        form = InvoiceTrxnForm(request.POST)
        form1 = TrxnForm(request.POST)
        form2 = PlayerTrxnForm(request.POST, instance=post)
        form3 = FieldReqStatForm(request.POST, instance=post1)
        form4 = PlayerTrxnForm(request.POST, instance=post3)
        form5 = ProformaStatusForm(request.POST, instance=post4)
        if form.is_valid():
            record = form.save(commit=False)
            record.field_request_id = proforma.field_request.id
            record.purpose_id = 2
            record.payer_id = online.id
            record.amount = proforma.amount
            record.status = 'Paid'
            record = form.save(commit=False)
            if Invoice.objects.filter(field_request_id=record.field_request_id).exists():
                messages.info(request, 'Invoice already actioned')
                return redirect(cancel)
            record.date_created = Now()
            record.author = request.user
            record.save()

            invoice = Invoice.objects.filter(field_request_id=record.field_request_id, purpose_id=record.purpose_id).last()
            post2 = get_object_or_404(Invoice, pk=invoice.id)
            if form1.is_valid():
                form1 = form1.save(commit=False)
                form1.invoice_ref = post2.id
                form1.payer_id = post2.payer.id
                form1.payee_id = 1
                form1.amount = post2.amount
                form1 = form1.save(commit=False)
                form1.payer_balance = post2.payer.trxn_balance - post2.amount
                form1.payee_balance = post2.amount + Player.objects.get(id=1).trxn_balance
                form1.purpose_id = 2
                form1.date_created = Now()
                form1.author = request.user
                form1.save()

                if form2.is_valid():
                    form2 = form2.save(commit=False)
                    form2.trxn_balance = form2.trxn_balance - form1.amount
                    form2.save()

                    if form3.is_valid():
                        form3 = form3.save(commit=False)
                        form3.status = 'Field'
                        form3.save()

                        if form4.is_valid():
                            form4 = form4.save(commit=False)
                            form4.trxn_balance = form4.trxn_balance + form1.amount
                            form4.save()

                            if form5.is_valid():
                                form5 = form5.save(commit=False)
                                form5.status = 'Active'
                                form5.save()

                            return redirect(cancel)

    form = InvoiceTrxnForm()
    form1 = TrxnForm()
    form2 = PlayerTrxnForm(instance=post)
    form3 = FieldReqStatForm(instance=post1)
    form4 = PlayerTrxnForm(instance=post3)
    form5 = ProformaStatusForm(instance=post4)
    context = {
        'proforma': proforma,
        'form':form,
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form3': form4,
        'form3': form5,
        'alerts': alerts,
        'cancel': cancel,
    }

    return render(request, 'investor/investview/field_proforma_pay.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_quote_counter(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    quote = FieldProviderQuote.objects.get(id=pk)
    post = get_object_or_404(FieldProviderQuote, id=quote.id)
    if request.method == 'POST':
        form = FieldReqCounterForm(request.POST, instance=post)
        if form.is_valid():
            form = form.save(commit=False)
            form.status = 'Counter Offer'
            form.save()

            return redirect('investor/investview/quote_detail.html', pk=quote.id)

    form = FieldReqCounterForm(instance=post)
    context = {
        'quote': quote,
        'form': form,
        'alerts': alerts,
    }

    return render(request, 'investor/investview/quote_counter.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_mandate_invoice_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    invoice = Invoice.objects.get(id=pk)

    context = {
        'invoice': invoice,
        'alerts': alerts,
    }

    return render(request, 'investor/investview/mandate/invoice_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_field_detail(request, pk):

    activity = Field.objects.get(id=pk)
    services = FiedlProviderRelation.objects.filter(field=activity)
    requirements = FiedlMineRequirements.objects.filter(field=activity)
    attachments = FieldAttachments.objects.filter(activity=activity)
    attach_filter = FieldAttachFilter(request.GET, queryset=attachments)
    acquitals = activity.fieldacquit_set.all()

    context = {
        'field_activity': activity,
        'services': services,
        'requirements': requirements,
        'attach_filter': attach_filter,
        'acquitals': acquitals,
    }

    return render(request, 'investor/investview/field/attach.html', context)


def investview_field_act(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    activity = Field.objects.get(id=pk)
    field_request = activity.field_request
    mandate = field_request.mandate
    mandate_request = mandate.mandate_request
    cart = mandate_request.cart_mine_match.cart_request
    attachments = activity.fieldattachments_set.all()
    attach_filter = FieldAttachFilter(request.GET, queryset=attachments)
    attach_count = len(attachments)

    context = {
        'field_activity': activity,
        'field_request': field_request,
        'mandate': mandate,
        'mandate_request': mandate_request,
        'cart': cart,
        'attach_filter': attach_filter,
        'attach_count': attach_count,
        'alerts': alerts,
    }

    return (request, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_field_act_attach(request, pk):

    context = {}
    investview_mandate(request, pk)

    return render(request, 'investor/investview/field/attach.html', context)


def investview_mandate(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate = Mandate.objects.get(id=pk)
    mandate_request = mandate.mandate_request
    cart = mandate.mandate_request.cart_mine_match.cart_request
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    field_requests = mandate.fieldreq_set.all()
    field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
    provider_filter = 0
    quote_count = 0
    if field_requests:
        for field_request in field_requests:
            field_request_list.append(field_request)
            proforma = field_request.fieldproforma_set.all().last()
            if proforma:
                quotes = proforma.fieldproviderquote_set.all()
                provider_filter = ServiceProvFilter(request.GET, queryset=quotes)
                quote_count = len(quotes)
                activity = proforma.field_set.all().last()
                if activity:
                    activities.append(activity)

    context = {
        'mandate': mandate,
        'mandate_request': mandate_request,
        'cart': cart,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'alerts': alerts,
    }

    return (request, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_mandate_field_act(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate = Mandate.objects.get(id=pk)
    mandate_request = mandate.mandate_request
    cart = mandate.mandate_request.cart_mine_match.cart_request
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    field_requests = mandate.fieldreq_set.all()
    field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
    provider_filter = None
    quote_count = 0
    services = None
    if field_requests:
        for field_request in field_requests:
            field_request_list.append(field_request)
            proforma = field_request.fieldproforma_set.all().last()
            services = field_request.serviceprovrequired_set.all()
            if services:
                for service in services:
                    quotes = service.fieldproviderquote_set.all()
                    provider_filter = ServiceQuoteFilter(request.GET, queryset=quotes)
                    quote_count = len(quotes)
            if proforma:
                activity = proforma.field_set.all().last()
                if activity:
                    activities.append([activity, proforma])

    context = {
        'mandate': mandate,
        'mandate_request': mandate_request,
        'cart': cart,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/mandate/field_activity.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_mandate_field_req(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    mandate = Mandate.objects.get(id=pk)
    mandate_request = mandate.mandate_request
    cart = mandate.mandate_request.cart_mine_match.cart_request
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    field_requests = mandate.fieldreq_set.all()
    field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
    provider_filter = None
    quote_count = 0
    services = None
    if field_requests:
        for field_request in field_requests:
            field_request_list.append(field_request)
            proforma = field_request.fieldproforma_set.all().last()
            services = field_request.serviceprovrequired_set.all()
            if services:
                for service in services:
                    quotes = service.fieldproviderquote_set.all()
                    provider_filter = ServiceQuoteFilter(request.GET, queryset=quotes)
                    quote_count = len(quotes)
            if proforma:
                activity = proforma.field_set.all().last()
                if activity:
                    activities.append([activity, proforma])

    context = {
        'mandate': mandate,
        'mandate_request': mandate_request,
        'cart': cart,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/mandate/services.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_mandate_field_quote(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    mandate = Mandate.objects.get(id=pk)
    mandate_request = mandate.mandate_request
    cart = mandate.mandate_request.cart_mine_match.cart_request
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    field_requests = mandate.fieldreq_set.all()
    field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
    provider_filter = None
    quote_count = 0
    services = None
    if field_requests:
        for field_request in field_requests:
            field_request_list.append(field_request)
            proforma = field_request.fieldproforma_set.all().last()
            services = field_request.serviceprovrequired_set.all()
            if services:
                for service in services:
                    quotes = service.fieldproviderquote_set.all()
                    provider_filter = ServiceQuoteFilter(request.GET, queryset=quotes)
                    quote_count = len(quotes)
            if proforma:
                activity = proforma.field_set.all().last()
                if activity:
                    activities.append([activity, proforma])

    context = {
        'mandate': mandate,
        'mandate_request': mandate_request,
        'cart': cart,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/mandate/field_quote.html', context)


def mandate_req(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate_request = MandateRequest.objects.get(id=pk)
    cart =  mandate_request.cart_mine_match.cart_request
    mandate = mandate_request.mandate_set.all().last()
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    provider_filter = 0
    quote_count = 0
    field_request_filter = 0
    if mandate:
        field_requests = mandate.fieldreq_set.all()
        field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
        if field_requests:
            for field_request in field_requests:
                field_request_list.append(field_request)
                proforma = field_request.fieldproforma_set.all().last()
                quotes = proforma.fieldproviderquote_set.all()
                provider_filter = ServiceProvFilter(request.GET, queryset=quotes)
                quote_count = len(quotes)
                if proforma:
                    activity = proforma.field_set.all().last()
                    if activity:
                        activities.append(activity)

    context = {
        'mandate_request': mandate_request,
        'mandate': mandate,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'cart': cart,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'alerts': alerts,
    }

    return render(request, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_mandate_request_field_act(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate_request = MandateRequest.objects.get(id=pk)
    cart =  mandate_request.cart_mine_match.cart_request
    mandate = mandate_request.mandate_set.all().last()
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    provider_filter = None
    quote_count = 0
    field_request_filter = None
    services = None
    quotes = None
    if mandate:
        field_requests = mandate.fieldreq_set.all()
        field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
        if field_requests:
            for field_request in field_requests:
                field_request_list.append(field_request)
                proforma = field_request.fieldproforma_set.all().last()
                services = field_request.serviceprovrequired_set.all()
                if services:
                    for service in services:
                        quotes = service.fieldproviderquote_set.all()
                        provider_filter = ServiceQuoteFilter(request.GET, queryset=quotes)
                        quote_count = len(quotes)
                if proforma:
                    actions = proforma.field_set.all()
                    if actions:
                        for activity in actions:
                            activities.append([activity, proforma])

    context = {
        'mandate_request': mandate_request,
        'mandate': mandate,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'cart': cart,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'alerts': alerts,
    }

    return render(request, 'investor/investview/mandate_request/field_activity.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_mandate_request_field_req(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate_request = MandateRequest.objects.get(id=pk)
    cart =  mandate_request.cart_mine_match.cart_request
    mandate = mandate_request.mandate_set.all().last()
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    provider_filter = None
    quote_count = 0
    field_request_filter = None
    actions = None
    services = None
    quotes = None
    if mandate:
        field_requests = mandate.fieldreq_set.all()
        field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
        if field_requests:
            for field_request in field_requests:
                field_request_list.append(field_request)
                proforma = field_request.fieldproforma_set.all().last()
                services = field_request.serviceprovrequired_set.all()
                if services:
                    for service in services:
                        quotes = service.fieldproviderquote_set.all()
                        if quotes:
                            provider_filter = ServiceProvFilter(request.GET, queryset=quotes)
                            quote_count = len(quotes)
                if proforma:
                    actions = proforma.field_set.all()
                    if actions:
                        for activity in actions:
                            activities.append(activity)

    context = {
        'mandate_request': mandate_request,
        'mandate': mandate,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'cart': cart,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/mandate_request/services.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_mandate_request_field_quote(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate_request = MandateRequest.objects.get(id=pk)
    cart =  mandate_request.cart_mine_match.cart_request
    mandate = mandate_request.mandate_set.all().last()
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    provider_filter = None
    quote_count = 0
    field_request_filter = None
    services = None
    quotes = None
    if mandate:
        field_requests = mandate.fieldreq_set.all()
        field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
        if field_requests:
            for field_request in field_requests:
                field_request_list.append(field_request)
                proforma = field_request.fieldproforma_set.all().last()
                services = field_request.serviceprovrequired_set.all()
                if services:
                    for service in services:
                        quotes = service.fieldproviderquote_set.all()
                        provider_filter = ServiceProvFilter(request.GET, queryset=quotes)
                        quote_count = len(quotes)
                if proforma:
                    actions = proforma.field_set.all()
                    if actions:
                        for activity in actions:
                            activities.append(activity)

    context = {
        'mandate_request': mandate_request,
        'mandate': mandate,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'cart': cart,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'alerts': alerts,
    }
    return render(request, 'investor/investview/mandate_request/field_quote.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investor_mandate_request_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    mandate_request = MandateRequest.objects.get(id=pk)
    cart =  mandate_request.cart_mine_match.cart_request
    mandate = mandate_request.mandate_set.all().last()
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    provider_filter = 0
    quote_count = 0
    field_request_filter = 0
    if mandate:
        field_requests = mandate.fieldreq_set.all()
        field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
        field_requests = field_request_filter.qs
        if field_requests:
            for field_request in field_requests:
                field_request_list.append(field_request)
                proforma = field_request.fieldproforma_set.all().last()
                services = ServiceProvRequired.objects.filter(field_request=field_request)
                if services:
                    for service in services:
                        quotes = service.fieldproviderquote_set.all()
                        provider_filter = ServiceProvFilter(request.GET, queryset=quotes)
                        quote_count = len(quotes)
                if proforma:
                    active_items = proforma.field_set.all()
                    if active_items:
                        for activity in active_items:
                            activities.append(activity)

    context = {
        'cart': cart,
        'mandate_request': mandate_request,
        'mandate': mandate,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'alerts': alerts,
    }
    return render(request, 'investor/mandate_request_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investor_mandate_request_field_req_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    mandate_request = MandateRequest.objects.get(id=pk)
    mine = mandate_request.minemandaterequest_set.all().last().mine
    mineloc = None
    polygon = None
    if MineLocation.objects.filter(name_id=mine.id):
        mineloc = MineLocation.objects.filter(name_id=mine.id).last()
    if mine.minepolygon_set.all():
        polygon = mine.minepolygon_set.all().last()
    cart =  mandate_request.cart_mine_match.cart_request
    mandate = mandate_request.mandate_set.all().last()
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    provider_filter = 0
    quote_count = 0
    field_request_filter = 0
    if mandate:
        field_requests = mandate.fieldreq_set.all()
        field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
        field_requests = field_request_filter.qs
        if field_requests:
            for field_request in field_requests:
                field_request_list.append(field_request)
                proforma = field_request.fieldproforma_set.all().last()
                services = ServiceProvRequired.objects.filter(field_request=field_request)
                if services:
                    for service in services:
                        quotes = service.fieldproviderquote_set.all()
                        provider_filter = ServiceProvFilter(request.GET, queryset=quotes)
                        quote_count = len(quotes)
                if proforma:
                    active_items = proforma.field_set.all()
                    if active_items:
                        for activity in active_items:
                            activities.append(activity)

    context = {
        'cart': cart,
        'mandate_request': mandate_request,
        'mandate': mandate,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'poly': polygon,
        'mineloc': mineloc,
        'alerts': alerts,
    }
    return render(request, 'investor/mandate_request_field_req.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investor_mandate_request_field_act_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate_request = MandateRequest.objects.get(id=pk)
    mine = mandate_request.minemandaterequest_set.all().last().mine
    mineloc = None
    polygon = None
    if MineLocation.objects.filter(name_id=mine.id):
        mineloc = MineLocation.objects.filter(name_id=mine.id).last()
    if mine.minepolygon_set.all():
        polygon = mine.minepolygon_set.all().last()
    cart =  mandate_request.cart_mine_match.cart_request
    mandate = mandate_request.mandate_set.all().last()
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    provider_filter = 0
    quote_count = 0
    field_request_filter = 0
    if mandate:
        field_requests = mandate.fieldreq_set.all()
        field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
        field_requests = field_request_filter.qs
        if field_requests:
            for field_request in field_requests:
                field_request_list.append(field_request)
                proforma = field_request.fieldproforma_set.all().last()
                services = ServiceProvRequired.objects.filter(field_request=field_request)
                if services:
                    for service in services:
                        quotes = service.fieldproviderquote_set.all()
                        provider_filter = ServiceProvFilter(request.GET, queryset=quotes)
                        quote_count = len(quotes)
                if proforma:
                    active_items = proforma.field_set.all()
                    if active_items:
                        for activity in active_items:
                            activities.append((activity, field_request))

    context = {
        'cart': cart,
        'mandate_request': mandate_request,
        'mandate': mandate,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'provider_filter': provider_filter,
        'quote_count': quote_count,
        'field_request_filter': field_request_filter,
        'poly': polygon,
        'mineloc': mineloc,
        'alerts': alerts,
    }
    return render(request, 'investor/mandate_request_field_act.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investor_mandate_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate = Mandate.objects.get(id=pk)
    mandate_request = mandate.mandate_request
    mine = mandate.minemandaterelation_set.all().last().mine
    mineloc = None
    polygon = None
    if MineLocation.objects.filter(name_id=mine.id):
        mineloc = MineLocation.objects.filter(name_id=mine.id).last()
    if mine.minepolygon_set.all():
        polygon = mine.minepolygon_set.all().last()
    cart =  mandate_request.cart_mine_match.cart_request
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    provider_filter = 0
    quote_list = []
    field_requests = mandate.fieldreq_set.all()
    field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
    field_requests = field_request_filter.qs
    if field_requests:
        for field_request in field_requests:
            field_request_list.append(field_request)
            proforma = field_request.fieldproforma_set.all().last()
            services = field_request.serviceprovrequired_set.all()
            if services:
                for service in services:
                    quotes = service.fieldproviderquote_set.all()
                    provider_filter = ServiceProvFilter(request.GET, queryset=quotes)
                    quote_list.append([service,quotes])
            if proforma:
                activity = proforma.field_set.all().last()
                if activity:
                    activities.append(activity)

    context = {
        'mandate_request': mandate_request,
        'mandate': mandate,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'cart': cart,
        'provider_filter': provider_filter,
        'quote_list': quote_list,
        'field_request_filter': field_request_filter,
        'poly': polygon,
        'mineloc': mineloc,
        'alerts': alerts,
    }

    return render(request, 'investor/mandate_detail.html', context)


def field_active(request, pk, template):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field_activity = Field.objects.filter(id=pk).last()
    attachments = None
    if field_activity.fieldattachments_set.all():
        attachments = field_activity.fieldattachments_set.all()
    attach_filter = ServiceAttachFilter(request.GET, queryset=attachments)
    attachments = attach_filter.qs
    attach_count = len(attachments)
    services = field_activity.fiedlproviderrelation_set.all()
    requirements = field_activity.fiedlminerequirements_set.all()
    acquitals = FieldAcquit.objects.filter(activity_id=field_activity.id)

    context = {
        'field_activity': field_activity,
        'attach_filter': attach_filter,
        'attach_count': attach_count,
        'acquitals': acquitals,
        'alerts': alerts,
        'services': services,
        'requirements': requirements,
    }

    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_activity_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field_activity = Field.objects.get(id=pk)
    attachments = field_activity.fieldattachments_set.all()
    attach_filter = ServiceAttachFilter(request.GET, queryset=attachments)
    attachments = attach_filter.qs
    attach_count = len(attachments)
    services = field_activity.fiedlproviderrelation_set.all()
    requirements = field_activity.fiedlminerequirements_set.all()
    acquit = FieldAcquit.objects.filter(activity=field_activity).last()

    context = {
        'field_activity': field_activity,
        'attach_filter': attach_filter,
        'attach_count': attach_count,
        'acquit': acquit,
        'alerts': alerts,
        'services': services,
        'requirements': requirements,
    }

    return render(request, 'field_activity_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_field_activity_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    field_activity = Field.objects.get(id=pk)
    attachments = field_activity.fieldattachments_set.filter(author=request.user)
    attach_filter = ServiceAttachFilter(request.GET, queryset=attachments)
    attachments = attach_filter.qs
    attach_count = len(attachments)
    acquit = FieldAcquit.objects.filter(activity=field_activity).last()

    context = {
        'field_activity': field_activity,
        'attach_filter': attach_filter,
        'attach_count': attach_count,
        'attachments': attachments,
        'acquit': acquit,
        'alerts': alerts,
    }

    return render(request, 'services/proview/field/detail_attach.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_activity_quotes(request, pk):

    context = {}
    field_active(request, pk)

    return render(request, 'field_activity_detail_tasks.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_activity_attach(request, pk):

    context = {}
    field_active(request, pk)

    return render(request, 'field_activity_detail_attach.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mandate_detail_field_activity(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate = Mandate.objects.get(id=pk)
    mine = mandate.mandate_request.minemandaterequest_set.all().last().mine
    mineloc = None
    polygon = None
    if MineLocation.objects.filter(name_id=mine.id):
        mineloc = MineLocation.objects.filter(name_id=mine.id).last()
    if mine.minepolygon_set.all():
        polygon = mine.minepolygon_set.all().last()
    mandate_request = mandate.mandate_request
    cart =  mandate_request.cart_mine_match.cart_request
    field_request_list = []
    field_request_count = len(field_request_list)
    activities = []
    activity_count = len(activities)
    provider_filter = 0
    quote_list = []
    field_requests = mandate.fieldreq_set.all()
    field_request_filter = InvestviewFieldReqFilter(request.GET, queryset=field_requests)
    field_requests = field_request_filter.qs
    if field_requests:
        for field_request in field_requests:
            field_request_list.append(field_request)
            proformas = field_request.fieldproforma_set.all()
            services = field_request.serviceprovrequired_set.all()
            if services:
                for service in services:
                    quotes = service.fieldproviderquote_set.all()
                    provider_filter = ServiceProvFilter(request.GET, queryset=quotes)
                    quote_list.append([service,quotes])
            if proformas:
                for proforma in proformas:
                    activity = proforma.field_set.all().last()
                    if activity:
                        activities.append(activity)

    context = {
        'mandate_request': mandate_request,
        'mandate': mandate,
        'field_request_list': field_request_list,
        'field_request_count': field_request_count,
        'activities': activities,
        'activity_count': activity_count,
        'cart': cart,
        'provider_filter': provider_filter,
        'quote_list': quote_list,
        'field_request_filter': field_request_filter,
        'poly': polygon,
        'mineloc': mineloc,
        'alerts': alerts,
    }
    return render(request, 'investor/mandate_detail_field_activity.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def get_field_quote(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    field_activity = Field.objects.get(id=pk)
    choices = ServiceProv.objects.all()
    choice_filter = ServiceChoiceFilter(request.GET, queryset=choices)
    choices = choice_filter.qs
    provider_count = len(choices)
    chosens = field_activity.fieldactivityqoutes_set.all()
    chosen = list(chosens)

    context = {
        'field_activity': field_activity,
        'choice_filter': choice_filter,
        'provider_count': provider_count,
        'chosens': chosens,
        'alerts': alerts,
    }

    return render(request, 'get_field_quotes.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_request_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    provider = player.serviceprov_set.all().last()
    field_request = FieldReq.objects.get(id=pk)
    service = None
    quote_count = 0
    quote_filter = None
    quotes = None
    activities = []
    activity_count = len(activities)
    proforma = None
    services = field_request.serviceprovrequired_set.all()
    if services:
        service = services.filter(field_request_id=field_request.id, provider_role_id=provider.rating.id).last()
        if service:
            if service.fieldproviderquote_set.all():
                quotes = service.fieldproviderquote_set.all()
                quote_filter = ServiceQuoteFilter(request.GET, queryset=quotes)
                quote_count = len(quotes)
    if field_request.fieldproforma_set.all():
        proforma = field_request.fieldproforma_set.all().last()
        if proforma.field_set.all():
            actions = proforma.field_set.all()
            for activity in actions:
                activities.append([activity, proforma])

    context = {
        'field_request': field_request,
        'activities': activities,
        'activity_count': activity_count,
        'quote_filter': quote_filter,
        'quote_count': quote_count,
        'quotes': quotes,
        'provider':provider,
        'services': services,
        'alerts': alerts,
    }
    return render(request, 'investor/field_request_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_request_detail_quote(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    field_request = FieldReq.objects.get(id=pk)
    quote_count = 0
    quotes = None
    activities = None
    activity_count = 0
    proforma = 0
    quote_list = []
    quotations = FieldProviderQuote.objects.all()
    quote_filter = ServiceQuoteFilter(request.GET, queryset=quotations)
    quotations = quote_filter.qs
    services = field_request.serviceprovrequired_set.all()
    if services:
        for service in services:
            if quotations.filter(service_ref_id=service.id):
                quotes = quotations.filter(service_ref_id=service.id)
                for quote in quotes:
                    quote_list.append(quote)
    if field_request.fieldproforma_set.all():
        proforma = field_request.fieldproforma_set.all().last()
        if proforma.field_set.all():
            activities = proforma.field_set.all()
            activity_count = len(activities)

    context = {
        'field_request': field_request,
        'activities': activities,
        'activity_count': activity_count,
        'quote_filter': quote_filter,
        'quote_count': quote_count,
        'quotes': quotes,
        'services': services,
        'quote_list': quote_list,
        'alerts': alerts,
    }
    return render(request, 'investor/field_request_detail_quote.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_mine_owner(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = Player.objects.get(pk=pk)
    if request.method == 'POST':
        form = MineOwnerForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner_id = player.id
            record.date_created = Now()
            record = form.save(commit=False)

            if MineOwnerRelation.objects.filter(mine_id=record.mine_id, status='Current').exists():
                messages.info(request, 'Mine can not be allocated to this entity')
                return render(request, 'mine_owner/add.html', {'form': form})

            record.author = request.user
            record.save()
            return redirect('player_detail.html', pk=pk)

    else:
        form = MineOwnerForm()

    context = {
        'form': form,
        'player': player,
        'alerts': alerts,
    }
    return render(request, 'mine_owner/add.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_service_provider(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = Player.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServiceProvForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.owner_id = player.id
            record.date_created = Now()
            record = form.save(commit=False)

            if ServiceProv.objects.filter(service_id=record.service.id, rating_id=record.rating.id).exists():
                messages.info(request, 'Mine can not be allocated to this entity')
                return render(request, 'services/add_provider.html', {'form': form})

            record.author = request.user
            record.save()
            return redirect('player_detail.html', pk=pk)

    else:
        form = ServiceProvForm()

    context = {
        'form': form,
        'player': player,
        'alerts': alerts,
    }
    return render(request, 'services/add_provider.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_submit_quote(request, pk):

    field_request = FieldReq.objects.get(pk=pk)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    provider = player.serviceprov_set.all().last()
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    service =field_request.serviceprovrequired_set.filter(provider_role_id=provider.rating.id).last()
    if request.method == 'POST':
        form = SubmitQuoteForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.service_ref_id = service.id
            record.provider_id = provider.id
            record.status = 'Submitted'
            record.date_created = Now()
            record = form.save(commit=False)

            if FieldProviderQuote.objects.filter(service_ref_id=service.id).exists():
                messages.info(request, 'Quote already submitted')
                context = {
                    'form': record,
                    'player': player,
                    'cancel': cancel,
                    'alerts': alerts,
                    'provider': provider,
                    'service': service,
                    'field_request': field_request,
                }
                return render(request, 'services/proview/submit_quote.html', context)

            record.author = request.user
            record.save()
            return redirect('services/proview/fieldreq/claims.html', pk=pk)

    else:
        form = SubmitQuoteForm()

    context = {
        'form': form,
        'player': player,
        'cancel': cancel,
        'alerts': alerts,
        'provider': provider,
        'service': service,
        'field_request': field_request,
    }
    return render(request, 'services/proview/submit_quote.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_accept_counter_offer(request, pk):

    quote = FieldProviderQuote.objects.get(pk=pk)
    post = get_object_or_404(FieldProviderQuote, pk=pk)
    post1 = get_object_or_404(ServiceProvRequired, id=quote.service_ref.id)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = FieldReqWinQteForm(request.POST)
        form1 = FieldServStatForm(request.POST, instance=post1)
        form2 = FieldProviderQuoteCounterForm(request.POST,instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            record.service_ref_id = quote.service_ref.id
            record.quote_id = quote.id
            record.date_created = Now()

            if form1.is_valid():
                form1 = form1.save(commit=False)
                if quote.service_ref.quantity == quote.service_ref.fieldreqwinqte_set.all().count:
                    form1.status = 'Completed'
                form1.save()

                if form2.is_valid():
                    form2 = form2.save(commit=False)
                    form2.cost = form2.counter_offer
                    form2.status = 'Success'
                    form2.save()

                    return redirect('services/proview/fieldreq/quote.html', pk=quote.service_ref.field_request.id)

    else:
        form = FieldReqWinQteForm()
        form1 = FieldServStatForm(instance=post)
        form2 = FieldProviderQuoteCounterForm(instance=post)

    context = {
        'quote': quote,
        'form': form,
        'form1': form1,
        'form2': form2,
        'player': player,
        'cancel': cancel,
        'alerts': alerts,
        'service': service,
    }
    return render(request, 'services/proview/accept_counter_offer.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_investor(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    player = Player.objects.get(pk=pk)
    if request.method == 'POST':
        form = InvestorForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.player_id = player.id
            record.date_created = Now()

            if Investor.objects.filter(player_id=record.player.id).exists():
                messages.info(request, 'Entity already registered as an investor')
                return render(request, 'investor/add.html', {'form': form})

            record.author = request.user
            record.save()
            return redirect('player_detail.html', pk=pk)

    else:
        form = InvestorForm()

    context = {
        'form': form,
        'player': player,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'investor/add.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_beacon(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    claim = MiningClaim.objects.get(pk=pk)
    beacons = claim.beacon_set.all()
    beacon_list = list(beacons)
    beacon_count = len(beacons)
    claim_poly = MiningClaimPolygon.objects.filter(name=claim).last()
    poly_object = None
    form1 = BeaconPolyForm(request.POST)
    if beacon_count > 2:
        if claim_poly:
            poly_object = get_object_or_404(MiningClaimPolygon, pk=claim_poly.id)
            form1 = BeaconPolyForm(request.POST, instance=poly_object)
    coordinate_list = []
    wkt = "SRID=4326;POLYGON(("
    claim_loc = None
    loc = None
    loc_obj = None
    mineloc = None
    beacon_wkt = 0
    last_beacon = None
    lat = 0
    long = 0
    cb = "))"
    sep = ", "
    blank = " "
    beac1 = None
    count = 0
    if beacons:
        claim_loc = Point(beacon_list[0].latitude, beacon_list[0].longitude)
        if claim.miningclaimlocation_set.all():
            loc = claim.miningclaimlocation_set.all().last()
            loc_obj = get_object_or_404(MiningClaimLocation, pk=loc.id)
            mineloc = loc_obj.lat_long

    if request.method == 'POST':
        form = BeaconForm(request.POST)
        if claim_poly:
            poly_object = get_object_or_404(MiningClaimPolygon, pk=claim_poly.id)
            form1 = BeaconPolyForm(request.POST, instance=poly_object)
        else:
            form1 = BeaconPolyForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mining_claim_id = claim.id
            record.date_created = Now()

            if Beacon.objects.filter(mining_claim_id=claim.id, latitude=record.latitude, longitude=record.longitude).exists():
                messages.info(request, 'Beacon already captured')
                form = BeaconForm()
                if claim_poly:
                    poly_object = get_object_or_404(MiningClaimPolygon, pk=claim_poly.id)
                    form1 = BeaconPolyForm(request.POST, instance=poly_object)
                else:
                    form1 = BeaconPolyForm(request.POST)
                context = {
                    'form': form,
                    'form1': form1,
                    'claim': claim,
                    'alerts': alerts,
                    'beacons': beacons,
                    'mineloc': mineloc,
                    'claim_loc': claim_loc,
                }
                return render(request, 'add_beacon.html', context)

            if beacons:
                record.symbol = beacons.last().symbol + 1
            else:
                record.symbol = 1

            record.author = request.user
            record.save()

            beacons = claim.beacon_set.all()
            beacon_list = list(beacons)
            claim_loc = [beacon_list[0].longitude, beacon_list[0].latitude]

            for beacon in beacons:
                coordinate_list.append([beacon.longitude, beacon.latitude])
            coordinate_list.append([beacons[0].longitude, beacons[0].latitude])

            if beacon_count > 2:
                if claim_poly:
                    if form1.is_valid():
                        poly_object = get_object_or_404(MiningClaimPolygon, pk=claim_poly.id)
                        obj = form1.save(commit=False)
                        obj.location = Polygon(coordinate_list, srid=4326)
                        obj.date_created = Now()
                        obj.save()
                else:
                    if form1.is_valid():
                        obj = form1.save(commit=False)
                        obj.name_id = claim.id
                        obj.location = Polygon(coordinate_list, srid=4326)
                        obj.date_created = Now()
                        obj.author = request.user
                        obj.save()

            return redirect('add_beacon.html', pk=pk)

    else:
        form = BeaconForm()
        if claim_poly:
            poly_object = get_object_or_404(MiningClaimPolygon, pk=claim_poly.id)
            form1 = BeaconPolyForm(instance=poly_object)
        else:
            form1 = BeaconPolyForm()

    context = {
        'form': form,
        'form1': form1,
        'claim': claim,
        'alerts': alerts,
        'beacons': beacons,
        'mineloc': mineloc,
        'claim_loc': claim_loc,
    }
    return render(request, 'add_beacon.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def new_sample(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    mine = Mine.objects.get(id=pk)
    sample_points = SamplePoint.objects.filter(mine=mine)
    # beacon_list = list(beacons)
    assay_object = None
    sample_point = None
    mine_poly = MinePolygon.objects.filter(name=mine).last()
    mineloc = MineLocation.objects.filter(name=mine).last().lat_long

    if request.method == 'POST':
        form = SamplePointForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = pk
            record.date_created = Now()
            record.author = request.user

            sample_point = SamplePoint.objects.filter(mine_id=pk, name=record.name, latitude=record.latitude, longitude=record.longitude).last()
            Assays.objects.Create(sample_date=record.sample_date, mineral_id=record.mineral, assay=record.assay, unit_id=record.unit, author=request.user)
            assay_object = Assays.objects.filter(sample_date=record.sample_date, mineral_id=record.mineral, assay=record.assay, unit_id=record.unit, author=request.user).last()

            SampleAssays.objects.Create(assay_id=assay_object.id, sample_point_id=sample_point.id)

            return redirect(cancel)

    else:
        form = SamplePointForm()

    context = {
        'form': form,
        'mine': mine,
        'sample_points': sample_points,
        'mine_poly': mine_poly,
        'mineloc': mineloc,
        'alerts': alerts,
        'cancel': cancel,
    }
    return render(request, 'new_sample.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def add_sample(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    sample_point = SamplePoint.objects.get(id=pk)
    mine = sample_point.mine
    sample_points = SamplePoint.objects.filter(mine=mine)
    # beacon_list = list(beacons)
    assay_object = None
    sample_point = None
    mine_poly = MinePolygon.objects.filter(name=mine).last()
    mineloc =  MineLocation.objects.filter(name=mine).last().lat_long

    if request.method == 'POST':
        form = AssayForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.date_created = Now()
            record.author = request.user

            assay_object = Assays.objects.filter(sample_date=record.sample_date, mineral_id=record.mineral, assay=record.assay, unit_id=record.unit, author=request.user).last()

            SampleAssays.objects.Create(assay_id=assay_object.id, sample_point_id=pk)

            return redirect(cancel)

    else:
        form = AssayForm()

    context = {
        'form': form,
        'mine': mine,
        'sample_points': sample_points,
        'mine_poly': mine_poly,
        'mineloc': mineloc,
        'alerts': alerts,
        'cancel': cancel,
    }
    return render(request, 'add_sample.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def claim_poly(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    claim = MiningClaim.objects.get(pk=pk)
    beacons = claim.beacon_set.all()
    beacon_list = list(beacons)
    beacon_count = len(beacons)
    claim_poly = MiningClaimPolygon.objects.filter(name=claim).last()
    coordinate_list = []
    claim_loc = None
    loc = None
    mineloc = None
    cb = "))"
    sep = ", "
    blank = " "
    geos_obj = 0
    if beacons:
        claim_loc = Point(beacon_list[0].longitude, beacon_list[0].latitude)
        if claim.miningclaimlocation_set.all():
            loc = claim.miningclaimlocation_set.all().last()
            loc_obj = get_object_or_404(MiningClaimLocation, pk=loc.id)
            mineloc = loc_obj.lat_long
        else:
            mineloc = claim_loc

        for beacon in beacons:
            coordinate_list.append([beacon.longitude, beacon.latitude])
        coordinate_list.append([beacons[0].longitude, beacons[0].latitude])
    geos_obj = 'GEOSGeometry("type": "Polygon", "coordinates": [{}])'.format(coordinate_list)

    if request.method == 'POST':
        form = DummyForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if claim_poly:
                poly_object = get_object_or_404(MiningClaimPolygon, pk=claim_poly.id)
                form1 = BeaconPolyForm(request.POST, instance=poly_object)
                if form1.is_valid():
                    record = form1.save(commit=False)
                    record.location = GEOSGeometry(form.location, srid=4326)
                    record.date_created = Now()
                    record.save()
            else:
                form1 = BeaconPolyForm(request.POST)
                if form1.is_valid():
                    obj = form1.save(commit=False)
                    obj.name_id = claim.id
                    obj.location = GEOSGeometry(form.location, srid=4326)
                    obj.date_created = Now()
                    obj.author = request.user
                    obj.save()

            return redirect('mining_claim_detail.html', pk=pk)

    else:
        form = DummyForm()
        if claim_poly:
            poly_object = get_object_or_404(MiningClaimPolygon, pk=claim_poly.id)
            form1 = BeaconPolyForm(instance=poly_object)
        else:
            form1 = BeaconPolyForm()

    context = {
        'form': form,
        'form1': form1,
        'claim': claim,
        'alerts': alerts,
        'beacons': beacons,
        'mineloc': mineloc,
        'claim_loc': claim_loc,
        'geos_obj': geos_obj,
        'coordinate_list': coordinate_list,
    }
    return render(request, 'add_claim_poly.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def claim_loc(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    claim = MiningClaim.objects.get(pk=pk)
    beacons = claim.beacon_set.all()
    claim_poly = MiningClaimPolygon.objects.filter(name=claim).last()
    poly_object = None
    coordinate_list = []
    claim_loc = None
    loc = None
    mineloc =  None
    loc_obj = None
    if claim_poly:
        poly_object = get_object_or_404(MiningClaimPolygon, pk=claim_poly.id)

    if request.method == 'POST':
        if claim.miningclaimlocation_set.all():
            loc = claim.miningclaimlocation_set.all().last()
            loc_obj = get_object_or_404(MiningClaimLocation, pk=loc.id)
            form = ClaimLocForm(request.POST, instance=loc_obj)
            if form.is_valid():
                record = form.save(commit=False)
                record.location = poly_object.location.centroid
                record.date_created = Now()
                record.save()

                return redirect('mining_claim_detail.html', pk=pk)
        else:
            form = ClaimLocForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.name_id = claim.id
                obj.location = poly_object.location.centroid
                obj.date_created = Now()
                obj.author = request.user
                obj.save()

            return redirect('mining_claim_detail.html', pk=pk)

    else:
        if claim.miningclaimlocation_set.all():
            form = ClaimLocForm(instance=loc_obj)
        else:
            form = ClaimLocForm()

    context = {
        'form': form,
        'claim': claim,
        'alerts': alerts,
        'mineloc': mineloc,
        'claim_loc': claim_loc,
    }
    return render(request, 'add_claim_loc.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def create_cart_request(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    investor = Investor.objects.get(id=pk)
    if request.method == 'POST':
        form = CartRequestForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.investor_id = investor.id
            record.date_created = Now()
            record = form.save(commit=False)

            # if Investor.objects.filter(player_id=record.player.id).exists():
            #     messages.info(request, 'Entity already registered as an investor')
            #     return render(request, 'investor/add.html', {'form': form})

            record.author = request.user
            record.save()
            return redirect('investor/mandate_detail.html', pk=investor.player.id)

    else:
        form = CartRequestForm()

    context = {
        'form': form,
        'investor': investor,
        'alerts': alerts,
    }
    return render(request, 'investor/cart_request_create.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def create_mandate_request(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    cart_mine_match = CartMineMatch.objects.get(id=pk)
    if request.method == 'POST':
        form = MandateRequestForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.cart_mine_match_id = cart_mine_match.id
            record.date_created = Now()
            record = form.save(commit=False)

            if MandateRequest.objects.filter(cart_mine_match_id=cart_mine_match.id, mine_id=record.mine_id, purpose=record.purpose, period=record.period).exists():
                messages.info(request, 'Mandate Request already exists')
                context = {
                    'form': form,
                    'cart_mine_match': cart_mine_match,
                    'alerts': alerts,
                }
                return render(request, 'investor/mandate_request_create', context)

            record.author = request.user
            record.save()
            return redirect('investor/face_detail.html', pk=cart_mine_match.cart_request.investor.id)

    else:
        form = MandateRequestForm()

    context = {
        'form': form,
        'cart_mine_match': cart_mine_match,
        'alerts': alerts,
    }
    return render(request, 'investor/mandate_request_create.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def create_work_history(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    player = Player.objects.get(id=pk)
    provider = ServiceProv.objects.filter(name=player).last()
    if request.method == 'POST':
        form = WorkHistoryForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.name_id = provider.id
            record.date_created = Now()
            record = form.save(commit=False)

            if SerProvProfile.objects.filter(principal=record.principal, title=record.title, from_date=record.from_date, to_date=record.to_date).exists():
                messages.info(request, 'Record already exists')
                context = {
                    'form': form,
                    'alerts': alerts,
                    'provider': provider,
                }
                return render(request, 'services/work_history.html', context)

            record.author = request.user
            record.save()
            return redirect('player_detail_service.html', pk=player.id)

    else:
        form = WorkHistoryForm()

    context = {
        'form': form,
        'alerts': alerts,
        'provider': provider,
    }
    return render(request, 'services/work_history.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def create_field_request(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate = Mandate.objects.get(id=pk)
    if request.method == 'POST':
        form = FieldReqForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mandate_id = mandate.id
            record.date_created = Now()
            record = form.save(commit=False)

            if record.period >= mandate.valid:
                messages.info(request, 'Field Request is out of Mandate period')
                context = {
                    'form': form,
                    'mandate': mandate,
                    'alerts': alerts,
                }
                return render(request, 'investor/field_request_create.html', context)

            if FieldReq.objects.filter(mandate_id=record.mandate.id, date_created=record.date_created, service=record.service, period=record.period).exists():
                messages.info(request, 'Field Request already exists')
                context = {
                    'form': form,
                    'mandate': mandate,
                    'alerts': alerts,
                }
                return render(request, 'investor/field_request_create.html', context)

            if record.service_req == 'False':
                record.status = 'Service Choice'
                record.author = request.user
                record.save()

                return redirect('investor/investview/mandate/services.html', pk=mandate.id)

            record.author = request.user
            record.save()
            return redirect('investor/investview/mandate/services.html', pk=mandate.id)

    else:
        form = FieldReqForm()

    context = {
        'form': form,
        'mandate': mandate,
        'alerts': alerts,
    }
    return render(request, 'investor/field_request_create.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def create_mandate(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate_request = MandateRequest.objects.get(id=pk)
    if request.method == 'POST':
        form = MandateForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mandate_request_id = mandate_request.id
            record.date_created = Now()
            record = form.save(commit=False)

            if Mandate.objects.filter(mandate_request_id=record.mandate_request.id).exists():
                messages.info(request, 'Mandate already exists')
                return redirect('investor/mandate_request_detail.html', pk=mandate_request.id)

            record.author = request.user
            record.save()

            mandate = Mandate.objects.filter(mandate_request_id=record.mandate_request.id).last()
            MineMandateRelation.objects.create(mine_id=mandate_request.mine.id, mandate_id=mandate.id, status=record.status, author=request.user)

            return redirect('investor/mandate_request_detail.html', pk=mandate_request.id)

    else:
        form = MandateForm()

    context = {
        'form': form,
        'mandate_request': mandate_request,
        'alerts': alerts,
    }
    return render(request, 'investor/mandate_create.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def create_cart_mine_match(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cart_request = CartRequest.objects.get(pk=pk)
    if request.method == 'POST':
        form = CartMineForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.cart_request_id = cart_request.id
            record.date_created = Now()
            record = form.save(commit=False)

            if CartMineMatch.objects.filter(cart_request_id=cart_request.id).exists():
                messages.info(request, 'Cart Match already exists')
                context = {
                    'form': form,
                    'cart_request': cart_request,
                    'alerts': alerts,
                }
                return render(request, 'investor/create_cart_mine_match.html', context)

            record.author = request.user
            record.save()
            return redirect('investor/cart_request_detail.html', pk=cart_request.id)

    else:
        form = CartMineForm()

    context = {
        'form': form,
        'cart_request': cart_request,
        'alerts': alerts,
    }
    return render(request, 'investor/create_cart_mine_match.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def edit_cart_mine_match(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    post = get_object_or_404(CartMineMatch, pk=pk)
    mine_match = CartMineMatch.objects.get(id=pk)

    if request.method == 'POST':
        form = CartMineForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            record.player_id = player.id
            record.date_created = Now()
            record = form.save(commit=False)

            if CartMineMatch.objects.filter(mines_id=record.mines.id, valid=record.valid).exists():
                messages.info(request, 'Mine Match already exists')
                context = {
                    'form': form,
                    'mine_match': mine_match,
                    'alerts': alerts,
                }
                return render(request, 'investor/edit_cart_mine_match.html', context)

            record.author = request.user
            record.save()

            old_list = CartMineRelation.objects.filter(cart_id=mine_match.id)
            for item in old_list:
                if item.mine.id is request.POST.getlist('mines'):
                    pass
                else:
                    item.delete()

            for mine in request.POST.getlist('mines'):
                if CartMineRelation.objects.filter(mine_id=mine.id, cart_id=mine_match.id).exists():
                    pass
                else:
                    CartMineRelation.objects.create(mine_id=mine.id, cart_id=mine_match.id, date_created=Now(), author=request.user)

            return redirect('investor/cart_request_detail.html', pk=mine_match.id)

    else:
        form = CartMineForm()

    context = {
        'form': form,
        'mine_match': mine_match,
        'alerts': alerts,
    }
    return render(request, 'investor/edit_cart_mine_match.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def service_face_detail(request, pk):

    provider = ServiceProv.objects.get(id=pk)
    pk = provider.name.id

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    player = Player.objects.get(id=pk)
    indi = 0
    corp = 0
    synd = 0
    if player.type == 'Individual':
        indi = IndRecord.objects.get(id=player.ref)
    elif player.type == 'Corporate':
        corp = CorpRecord.objects.get(id=player.ref)
    else:
        synd = Syndicate.objects.get(id=player.ref)

    mines = MineOwnerRelation.objects.filter(owner=player)
    mine_filter = PlayerMineFilter(request.GET, queryset=mines)
    mine_count = len(mines)
    investments = Investor.objects.filter(player=player).last()
    if investments:
        investor_status = 'Investor'
    else:
        investor_status = 'Not Investor'

    carts = CartRequest.objects.filter(investor_id=pk)
    cart_filter = CartRequestFilter(request.GET, queryset=carts)
    carts = cart_filter.qs
    services = ServiceProv.objects.filter(name=player)
    service_count = len(services)
    trxn_list = []
    transactions = Trxns.objects.all()
    trxn_filter = TrxnFilter(request.GET, queryset=transactions)
    transactions = trxn_filter.qs
    for actor in transactions:
        if actor.payer == player:
            trxn_list.append([player, '0'])
        elif actor.payee == player:
            trxn_list.append([player, '1'])
        else:
            pass
    receipts = []
    item = 0
    invoices = Invoice.objects.filter(payer=player)
    invoice_filter = InvoiceOwnerFilter(request.GET, queryset=invoices)
    if invoices:
        for invoice in invoices:
            item = invoice.receipt_set.all().last()
            receipts.append([invoice, item])

    payment_count = len(trxn_list)
    receipts_list = []
    receipt_count = len(receipts_list)
    for transact in Trxns.objects.filter(payer=player):
        receipt = Receipt.objects.filter(trxn_ref=transact).last()
        receipts_list.append(receipt)

    context = {
        'player': player,
        'provider': provider,
        'mines': mines,
        'mine_filter': mine_filter,
        'mine_count': mine_count,
        'investments': investments,
        'services': services,
        'service_count': service_count,
        'payments': trxn_list,
        'payment_count': payment_count,
        'receipts': receipts,
        'receipt_count': receipt_count,
        'investor_status': investor_status,
        'carts': carts,
        'cart_filter': cart_filter,
        'trxn_filter': trxn_filter,
        'invoice_filter': invoice_filter,
        'indi': indi,
        'corp': corp,
        'synd': synd,
        'alerts': alerts,
    }

    return render(request, 'player_detail_service.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_face_detail(request):

    player = PlayerUserRelation.objects.filter(user=request.user).last().player
    context = {}
    pk = player.id
    player(request, pk)
    alerts = Alerts.objects.filter(status='Active')
    context['alerts'] = alerts

    return render(request, 'player_detail_investor.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_mines(request):

    mines = 0
    mine_filter = 0
    mine_count = 0
    investments = 0
    services = 0
    service_count = 0
    payment_count = 0
    receipts = 0
    receipt_count = 0
    investor_status = 0
    carts = 0
    cart_filter = 0
    trxn_filter = 0
    invoice_filter = 0
    indi = 0
    corp = 0
    synd = 0

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    pk = player.id
    player(pk)
    alerts = Alerts.objects.filter(status='Active')


    context = {
        'player': player,
        'mines': mines,
        'mine_filter': mine_filter,
        'mine_count': mine_count,
        'investments': investments,
        'services': services,
        'service_count': service_count,
        'payments': trxn_list,
        'payment_count': payment_count,
        'receipts': receipts,
        'receipt_count': receipt_count,
        'investor_status': investor_status,
        'carts': carts,
        'cart_filter': cart_filter,
        'trxn_filter': trxn_filter,
        'invoice_filter': invoice_filter,
        'indi': indi,
        'corp': corp,
        'synd': synd,
        'alerts': alerts,
    }

    return render(request, 'mine_owner/mines.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mineview_erp(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    mineral_production = []
    ore_production = []
    waste_production = []

    for prod in mine.mineproduction_set.filter(material='Mineral'):
        produce = [prod.mineral, prod.quantity]
        n = 0
        for item in mineral_production:
            if item:
                if produce[0] == item[0]:
                    mineral_production[n][1] = item[1] + produce[1]
                else:
                    mineral_production.append(produce)
            else:
                mineral_production.append(produce)
            n += 1

    for prod in mine.mineproduction_set.filter(material='Ore'):
        produce = [prod.mineral, prod.quantity]
        n = 0
        for item in ore_production:
            if item:
                if produce[0] == item[0]:
                    ore_production[n][1] = item[1] + produce[1]
                else:
                    ore_production.append(produce)
            else:
                ore_production.append(produce)
            n += 1

    for prod in mine.mineproduction_set.filter(material='Waste'):
        produce = [prod.mineral, prod.quantity]
        n = 0
        for item in waste_production:
            if item:
                if produce[0] == item[0]:
                    waste_production[n][1] = item[1] + produce[1]
                else:
                    waste_production.append(produce)
            else:
                waste_production.append(produce)
            n += 1

    reports = mine.minereports_set.all()[:2]
    attachments = mine.minecertificates_set.all()[:2]
    visit_requests_list = []
    visit_req_count = len(visit_requests_list)
    field_proforma_list = []
    field_proforma_count = len(field_proforma_list)
    visit_list = []
    visit_count = len(visit_list)
    field_invoice_list = []
    field_invoice_count = len(field_invoice_list)
    mandate_list = []
    mandate_count = len(mandate_list)
    mandate_request_list = []
    mandate_request_count = len(mandate_request_list)

    claims = MineClaimRelation.objects.filter(mine=mine)
    claims_filter = ClaimsFilter(request.GET, queryset=claims)
    minerals = MineMineral.objects.filter(mine_id=pk)
    cart_matches = CartMineRelation.objects.filter(mine=mine)
    cart_filter = CartMatchFilter(request.GET, queryset=claims)
    cart_match_count = cart_matches.count
    production = 0
    works = 0
    labour = 0
    plant = 0
    mobile = 0

    if mine.mineworks_set.all():
        works = mine.mineworks_set.all()
    if mine.minelabour_set.all():
        labour = mine.minelabour_set.all().last()
    if mine.mineplant_set.all():
        plant = mine.mineplant_set.all()
    if mine.mineyellowplant_set.all():
        mobile = mine.mineyellowplant_set.all()

    mandate_request = 0
    mandate = 0
    visit_req = 0
    if cart_matches:
        for cart_match in cart_matches:
            mandate_request = MineMandateRequest.objects.filter(mandate_request=cart_match.cart.mandaterequest_set.all().last(), mine=mine).last()
            if mandate_request:
                mandate_request_list.append(cart_match, mandate_request)
                mandate = MineMandateRelation.objects.filter(mine=mine).last()
                if mandate:
                    mandate_list.append(cart_match, mandate_request, mandate)
                    visit_requests = FieldReq.objects.filter(mandate=mandate)
                    visit_request_filter = FieldReqFilter(request.GET, queryset=visit_requests)
                    visit_requests = visit_request_filter.qs
                    visit_req_count = visit_requests.count
                    if visit_requests:
                        for visit_req in visit_requests:
                            field_proforma = FieldProforma.objects.filter(field_request=visit_req).last()
                            visit_requests_list.append([cart_match, mandate_request, mandate, visit_req])
                            if field_proforma:
                                field_invoice = FieldInvoice.objects.filter(proforma=field_proforma).last()
                                visit = Field.objects.filter(proforma=field_proforma).last()
                                field_proforma_list.append([cart_match, mandate_request, mandate, visit_req,
                                                           field_proforma])
                                if field_invoice:
                                    field_invoice_list.append([cart_match, mandate_request, mandate, visit_req,
                                                              field_proforma, field_invoice])
                                if visit:
                                    visit_list.append([cart_match, mandate_request, mandate, visit_req, field_proforma,
                                                      visit])

    context = {
        'mine': mine,
        'claims_filter': claims_filter,
        'minerals': minerals,
        'mandate_count': mandate_count,
        'visit_req_count': visit_req_count,
        'cart_match_count': cart_match_count,
        'visit_count': visit_count,
        'field_proforma_count': field_proforma_count,
        'visit_requests_list': visit_requests_list,
        'field_proforma_list': field_proforma_list,
        'visit_list': visit_list,
        'field_invoice_list': field_invoice_list,
        'field_invoice_count': field_invoice_count,
        'mandate_list': mandate_list,
        'mandate_request_list': mandate_request_list,
        'mandate_request_count': mandate_request_count,
        'filter': cart_filter,
        'production': production,
        'works': works,
        'labour': labour,
        'plant': plant,
        'mobile': mobile,
        'reports': reports,
        'attachments': attachments,
        'mineral_production':mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'alerts': alerts,
    }
    return render(request, 'mine_owner/mineview/erp.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_mineview(request, pk, template):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    mine = Mine.objects.get(id=pk)
    mine_area = 0
    mineloc = MineLocation.objects.filter(name_id=mine.id).last()
    polygon = mine.minepolygon_set.all().last()
    works_filter = None
    plant_filter = None
    mobile_filter = None

    records = mine.minereports_set.all()
    report_filter = MineOwnerReportFilter(request.GET, queryset=records)
    records = report_filter.qs
    report_count = len(records)

    reports = records[:2]
    certs = mine.minecertificates_set.all()
    cert_filter = MineOwnerCertificateFilter(request.GET, queryset=certs)
    certificates = cert_filter.qs
    certificate_count = len(certificates)
    attachments = certs[:2]
    visit_requests_list = []
    visit_req_count = len(visit_requests_list)
    field_proforma_list = []
    field_proforma_count = len(field_proforma_list)
    visit_list = []
    visit_count = len(visit_list)
    field_invoice_list = []
    field_invoice_count = len(field_invoice_list)
    mandate_list = []
    mandate_count = len(mandate_list)
    mandate_request_list = []
    mandate_request_count = len(mandate_request_list)

    claims = MineClaimRelation.objects.filter(mine=mine)
    claims_filter = ClaimsFilter(request.GET, queryset=claims)
    claims = claims_filter.qs
    claimpoly = []
    for claim in claims:
        mine_area = mine_area + claim.claim.area
        if claim.claim.miningclaimpolygon_set.all():
            polygon = claim.claim.miningclaimpolygon_set.all().last()
            claimpoly.append(polygon)

    minerals = MineMineral.objects.filter(mine_id=pk)
    cart_matches = CartMineRelation.objects.filter(mine=mine)
    cart_filter = CartMatchFilter(request.GET, queryset=claims)
    cart_match_count = cart_matches.count
    production = None
    works = None
    labour = None
    plant = None
    mobile = None
    mineral_production = []
    ore_production = 0
    waste_production = 0
    products = mine.mineproduction_set.all()
    mineral_count = len(products.filter(material='Mineral'))
    ore_count = len(products.filter(material='Ore'))
    waste_count = len(products.filter(material='Waste'))
    filter = MoreProductionFilter(request.GET, queryset=products)
    products = filter.qs
    minerals = 0
    ore = 0
    waste = 0
    mineral_set = ['all',]
    units_set = []
    i = 0
    if mine.mineproduction_set.all():
        production = mine.mineproduction_set.all()
        for prod in production:
            if prod.mineral not in mineral_set:
                mineral_set.append(prod.mineral)
                mineral_production.append([prod.mineral, prod.quantity, prod.unit])
            else:
                i = mineral_set.index(prod.mineral)
                if prod.material == 'mineral':
                    if prod.mineral != 'all':
                        mineral_production[i][1] = mineral_production[i][1] + prod.quantity
                    else:
                        if prod.material == 'ore':
                            ore_production += prod.quantity
                        else:
                            waste_production += prod.quantity

    if mine.mineworks_set.all():
        works = mine.mineworks_set.all()
        works_filter = MineviewWorksFilter(request.GET, queryset=works)
        works = works_filter.qs
    if mine.minelabour_set.all():
        labour = mine.minelabour_set.all().last()
    if mine.mineplant_set.all():
        plant = mine.mineplant_set.all()
        plant_filter = MineviewPlantFilter(request.GET, queryset=plant)
        plant = plant_filter.qs
    if mine.mineyellowplant_set.all():
        mobile = mine.mineyellowplant_set.all()
        mobile_filter = MineviewMobileFilter(request.GET, queryset=mobile)
        mobile = mobile_filter.qs

    mandate_request = 0
    mandate = 0
    visit_req = 0
    if cart_matches:
        for cart_match in cart_matches:
            mandate_request = MineMandateRequest.objects.filter(mandate_request=cart_match.cart.mandaterequest_set.all().last(), mine=mine).last()
            if mandate_request:
                mandate_request_list.append([cart_match, mandate_request])
                mandate = MineMandateRelation.objects.filter(mine=mine).last()
                if mandate:
                    mandate_list.append([cart_match, mandate_request, mandate])
                    visit_requests = FieldReq.objects.filter(mandate=mandate)
                    visit_request_filter = FieldReqFilter(request.GET, queryset=visit_requests)
                    visit_requests = visit_request_filter.qs
                    visit_req_count = visit_requests.count
                    if visit_requests:
                        for visit_req in visit_requests:
                            field_proforma = FieldProforma.objects.filter(field_request=visit_req).last()
                            visit_requests_list.append([cart_match, mandate_request, mandate, visit_req])
                            if field_proforma:
                                field_invoice = FieldInvoice.objects.filter(proforma=field_proforma).last()
                                visit = Field.objects.filter(proforma=field_proforma).last()
                                field_proforma_list.append([cart_match, mandate_request, mandate, visit_req,
                                                           field_proforma])
                                if field_invoice:
                                    field_invoice_list.append([cart_match, mandate_request, mandate, visit_req,
                                                              field_proforma, field_invoice])
                                if visit:
                                    visit_list.append([cart_match, mandate_request, mandate, visit_req, field_proforma,
                                                      visit])

    context = {
        'mine': mine,
        'mine_area': mine_area,
        'poly': polygon,
        'mineloc': mineloc,
        'claims_filter': claims_filter,
        'claims': claimpoly,
        'minerals': minerals,
        'mandate_count': mandate_count,
        'visit_req_count': visit_req_count,
        'cart_match_count': cart_match_count,
        'visit_count': visit_count,
        'field_proforma_count': field_proforma_count,
        'visit_requests_list': visit_requests_list,
        'field_proforma_list': field_proforma_list,
        'visit_list': visit_list,
        'field_invoice_list': field_invoice_list,
        'field_invoice_count': field_invoice_count,
        'mandate_list': mandate_list,
        'mandate_request_list': mandate_request_list,
        'mandate_request_count': mandate_request_count,
        'filter': cart_filter,
        'mineral_count': mineral_count,
        'ore_count': ore_count,
        'waste_count': waste_count,
        'mineral_production': mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'mineral_set': mineral_set,
        'units_set': units_set,
        'ore': ore,
        'waste': waste,
        'works': works,
        'labour': labour,
        'plant': plant,
        'mobile': mobile,
        'reports': reports,
        'attachments': attachments,
        'alerts': alerts,
        'report_filter': report_filter,
        'report_count': report_count,
        'cert_filter': cert_filter,
        'certificate_count': certificate_count,
        'works_filter': works_filter,
        'plant_filter': plant_filter,
        'mobile_filter': mobile_filter,
        'cancel': cancel,
    }
    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_mineview_field(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    mineral_production = []
    ore_production = []
    waste_production = []

    for prod in mine.mineproduction_set.filter(material='Mineral'):
        produce = [prod.mineral, prod.quantity]
        n = 0
        for item in mineral_production:
            if item:
                if produce[0] == item[0]:
                    mineral_production[n][1] = item[1] + produce[1]
                else:
                    mineral_production.append(produce)
            else:
                mineral_production.append(produce)
            n += 1

    for prod in mine.mineproduction_set.filter(material='Ore'):
        produce = [prod.mineral, prod.quantity]
        n = 0
        for item in ore_production:
            if item:
                if produce[0] == item[0]:
                    ore_production[n][1] = item[1] + produce[1]
                else:
                    ore_production.append(produce)
            else:
                ore_production.append(produce)
            n += 1

    for prod in mine.mineproduction_set.filter(material='Waste'):
        produce = [prod.mineral, prod.quantity]
        n = 0
        for item in waste_production:
            if item:
                if produce[0] == item[0]:
                    waste_production[n][1] = item[1] + produce[1]
                else:
                    waste_production.append(produce)
            else:
                waste_production.append(produce)
            n += 1

    reports = mine.minereports_set.all()[:2]
    attachments = mine.minecertificates_set.all()[:2]
    visit_requests_list = []
    visit_req_count = len(visit_requests_list)
    field_proforma_list = []
    field_proforma_count = len(field_proforma_list)
    visit_list = []
    visit_count = len(visit_list)
    field_invoice_list = []
    field_invoice_count = len(field_invoice_list)
    mandate_list = []
    mandate_count = len(mandate_list)
    mandate_request_list = []
    mandate_request_count = len(mandate_request_list)

    claims = MineClaimRelation.objects.filter(mine=mine)
    claims_filter = ClaimsFilter(request.GET, queryset=claims)
    minerals = MineMineral.objects.filter(mine_id=pk)
    cart_matches = CartMineRelation.objects.filter(mine=mine)
    cart_filter = CartMatchFilter(request.GET, queryset=claims)
    cart_match_count = cart_matches.count
    production = 0
    works = 0
    labour = 0
    plant = 0
    mobile = 0

    if mine.mineworks_set.all():
        works = mine.mineworks_set.all()
    if mine.minelabour_set.all():
        labour = mine.minelabour_set.all().last()
    if mine.mineplant_set.all():
        plant = mine.mineplant_set.all()
    if mine.mineyellowplant_set.all():
        mobile = mine.mineyellowplant_set.all()

    mandate_request = 0
    mandate = 0
    visit_req = 0
    if cart_matches:
        for cart_match in cart_matches:
            mandate_request = MineMandateRequest.objects.filter(mandate_request=cart_match.cart.mandaterequest_set.all().last(), mine=mine).last()
            if mandate_request:
                mandate_request_list.append(cart_match, mandate_request)
                mandate = MineMandateRelation.objects.filter(mine=mine).last()
                if mandate:
                    mandate_list.append(cart_match, mandate_request, mandate)
                    visit_requests = FieldReq.objects.filter(mandate=mandate)
                    visit_request_filter = FieldReqFilter(request.GET, queryset=visit_requests)
                    visit_requests = visit_request_filter.qs
                    visit_req_count = visit_requests.count
                    if visit_requests:
                        for visit_req in visit_requests:
                            field_proforma = FieldProforma.objects.filter(field_request=visit_req).last()
                            visit_requests_list.append(cart_match, mandate_request, mandate, visit_req)
                            if field_proforma:
                                field_invoice = FieldInvoice.objects.filter(proforma=field_proforma).last()
                                visit = Field.objects.filter(proforma=field_proforma).last()
                                field_proforma_list.append(cart_match, mandate_request, mandate, visit_req,
                                                           field_proforma)
                                if field_invoice:
                                    field_invoice_list.append(cart_match, mandate_request, mandate, visit_req,
                                                              field_proforma, field_invoice)
                                if visit:
                                    visit_list.append(cart_match, mandate_request, mandate, visit_req, field_proforma,
                                                      visit)

    context = {
        'mine': mine,
        'claims_filter': claims_filter,
        'minerals': minerals,
        'mandate_count': mandate_count,
        'visit_req_count': visit_req_count,
        'cart_match_count': cart_match_count,
        'visit_count': visit_count,
        'field_proforma_count': field_proforma_count,
        'visit_requests_list': visit_requests_list,
        'field_proforma_list': field_proforma_list,
        'visit_list': visit_list,
        'field_invoice_list': field_invoice_list,
        'field_invoice_count': field_invoice_count,
        'mandate_list': mandate_list,
        'mandate_request_list': mandate_request_list,
        'mandate_request_count': mandate_request_count,
        'filter': cart_filter,
        'production': production,
        'works': works,
        'labour': labour,
        'plant': plant,
        'mobile': mobile,
        'reports': reports,
        'attachments': attachments,
        'mineral_production':mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'alerts': alerts,
    }

    return render(request, 'mine_owner/mineview/field.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_mineview_reports(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine= Mine.objects.get(id=pk)
    records = MineReports.objects.filter(mine_id=mine.id)
    filter = MineOwnerReportFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    report_count = len(records)
    certificates = MineCertificates.objects.filter(mine=mine)
    cert_filter = MineOwnerCertificateFilter(request.GET, queryset=certificates)
    certificates = cert_filter.qs
    certificate_count = len(certificates)

    context = {
        'filter': filter,
        'page_obj': page_obj,
        'mine': mine,
        'report_count': report_count,
        'cert_filter': cert_filter,
        'certificate_count': certificate_count,
        'alerts': alerts,
    }

    return render(request, 'mine_owner/mineview_reports.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_mineview_mandates(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)
    mineral_production = []
    ore_production = []
    waste_production = []

    for prod in mine.mineproduction_set.filter(material='Mineral'):
        produce = [prod.mineral, prod.quantity]
        n = 0
        for item in mineral_production:
            if item:
                if produce[0] == item[0]:
                    mineral_production[n][1] = item[1] + produce[1]
                else:
                    mineral_production.append(produce)
            else:
                mineral_production.append(produce)
            n += 1

    for prod in mine.mineproduction_set.filter(material='Ore'):
        produce = [prod.mineral, prod.quantity]
        n = 0
        for item in ore_production:
            if item:
                if produce[0] == item[0]:
                    ore_production[n][1] = item[1] + produce[1]
                else:
                    ore_production.append(produce)
            else:
                ore_production.append(produce)
            n += 1

    for prod in mine.mineproduction_set.filter(material='Waste'):
        produce = [prod.mineral, prod.quantity]
        n = 0
        for item in waste_production:
            if item:
                if produce[0] == item[0]:
                    waste_production[n][1] = item[1] + produce[1]
                else:
                    waste_production.append(produce)
            else:
                waste_production.append(produce)
            n += 1

    reports = mine.minereports_set.all()[:2]
    attachments = mine.minecertificates_set.all()[:2]
    visit_requests_list = []
    visit_req_count = len(visit_requests_list)
    field_proforma_list = []
    field_proforma_count = len(field_proforma_list)
    visit_list = []
    visit_count = len(visit_list)
    field_invoice_list = []
    field_invoice_count = len(field_invoice_list)
    mandate_list = []
    mandate_count = len(mandate_list)
    mandate_request_list = []
    mandate_request_count = len(mandate_request_list)

    claims = MineClaimRelation.objects.filter(mine=mine)
    claims_filter = ClaimsFilter(request.GET, queryset=claims)
    minerals = MineMineral.objects.filter(mine_id=pk)
    cart_matches = CartMineRelation.objects.filter(mine=mine)
    cart_filter = CartMatchFilter(request.GET, queryset=claims)
    cart_match_count = cart_matches.count
    production = 0
    works = 0
    labour = 0
    plant = 0
    mobile = 0

    if mine.mineworks_set.all():
        works = mine.mineworks_set.all()
    if mine.minelabour_set.all():
        labour = mine.minelabour_set.all().last()
    if mine.mineplant_set.all():
        plant = mine.mineplant_set.all()
    if mine.mineyellowplant_set.all():
        mobile = mine.mineyellowplant_set.all()

    mandate_request = 0
    mandate = 0
    visit_req = 0
    if cart_matches:
        for cart_match in cart_matches:
            mandate_request = MineMandateRequest.objects.filter(mandate_request=cart_match.cart.mandaterequest_set.all().last(), mine=mine).last()
            if mandate_request:
                mandate_request_list.append(cart_match, mandate_request)
                mandate = MineMandateRelation.objects.filter(mine=mine).last()
                if mandate:
                    mandate_list.append(cart_match, mandate_request, mandate)
                    visit_requests = FieldReq.objects.filter(mandate=mandate)
                    visit_request_filter = FieldReqFilter(request.GET, queryset=visit_requests)
                    visit_requests = visit_request_filter.qs
                    visit_req_count = visit_requests.count
                    if visit_requests:
                        for visit_req in visit_requests:
                            field_proforma = FieldProforma.objects.filter(field_request=visit_req).last()
                            visit_requests_list.append(cart_match, mandate_request, mandate, visit_req)
                            if field_proforma:
                                field_invoice = FieldInvoice.objects.filter(proforma=field_proforma).last()
                                visit = Field.objects.filter(proforma=field_proforma).last()
                                field_proforma_list.append(cart_match, mandate_request, mandate, visit_req,
                                                           field_proforma)
                                if field_invoice:
                                    field_invoice_list.append(cart_match, mandate_request, mandate, visit_req,
                                                              field_proforma, field_invoice)
                                if visit:
                                    visit_list.append(cart_match, mandate_request, mandate, visit_req, field_proforma,
                                                      visit)

    context = {
        'mine': mine,
        'claims_filter': claims_filter,
        'minerals': minerals,
        'mandate_count': mandate_count,
        'visit_req_count': visit_req_count,
        'cart_match_count': cart_match_count,
        'visit_count': visit_count,
        'field_proforma_count': field_proforma_count,
        'visit_requests_list': visit_requests_list,
        'field_proforma_list': field_proforma_list,
        'visit_list': visit_list,
        'field_invoice_list': field_invoice_list,
        'field_invoice_count': field_invoice_count,
        'mandate_list': mandate_list,
        'mandate_request_list': mandate_request_list,
        'mandate_request_count': mandate_request_count,
        'filter': cart_filter,
        'production': production,
        'works': works,
        'labour': labour,
        'plant': plant,
        'mobile': mobile,
        'reports': reports,
        'attachments': attachments,
        'mineral_production':mineral_production,
        'ore_production': ore_production,
        'waste_production': waste_production,
        'alerts': alerts,
    }

    return render(request, 'mine_owner/mineview/mandates.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_claimview(request, pk, template):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    claim = MiningClaim.objects.get(pk=pk)
    beacons = Beacon.objects.filter(mining_claim=claim)
    mineloc = MiningClaimLocation.objects.filter(name_id=claim.id).last()
    polygon = claim.miningclaimpolygon_set.all().last()
    beacon_count = beacons.count
    certificate = claim.claimregcert_set.all().last()

    context = {
        'claim': claim,
        'poly': polygon,
        'mineloc': mineloc,
        'beacons': beacons,
        'beacon_count': beacon_count,
        'certificate': certificate,
        'alerts': alerts,
        'cancel': cancel,
    }

    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investor_profile(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    indi = 0
    synd = 0
    corp = 0
    if IndRecord.objects.filter(id=player.ref):
        indi = IndRecord.objects.get(id=player.ref)
    if Syndicate.objects.filter(id=player.ref):
        synd = Syndicate.objects.get(id=player.ref)
    if CorpRecord.objects.filter(id=player.ref):
        corp = CorpRecord.objects.get(id=player.ref)

    context = {
        'player': player,
        'indi': indi,
        'synd': synd,
        'corp': corp,
        'alerts': alerts,
    }

    return render(request, 'investor/profile.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def provider_profile(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    provider = player.serviceprov_set.all().last()
    indi = 0
    synd = 0
    corp = 0
    if IndRecord.objects.filter(id=player.ref):
        indi = IndRecord.objects.get(id=player.ref)
    if Syndicate.objects.filter(id=player.ref):
        synd = Syndicate.objects.get(id=player.ref)
    if CorpRecord.objects.filter(id=player.ref):
        corp = CorpRecord.objects.get(id=player.ref)
    history = provider.serprovprofile_set.all

    context = {
        'player': player,
        'indi': indi,
        'synd': synd,
        'corp': corp,
        'alerts': alerts,
        'provider': provider,
        'history': history,
    }

    return render(request, 'services/proview/profile.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_profile(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    indi = 0
    synd = 0
    corp = 0
    if IndRecord.objects.filter(id=player.ref):
        indi = IndRecord.objects.get(id=player.ref)
    if Syndicate.objects.filter(id=player.ref):
        synd = Syndicate.objects.get(id=player.ref)
    if CorpRecord.objects.filter(id=player.ref):
        corp = CorpRecord.objects.get(id=player.ref)

    context = {
        'player': player,
        'indi': indi,
        'synd': synd,
        'corp': corp,
        'alerts': alerts,
    }

    return render(request, 'mine_owner/profile.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_accounts(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    trxn_list = []
    transactions = Trxns.objects.filter(Q(payer=player) | Q(payee=player))
    trxn_filter = TrxnFilter(request.GET, queryset=transactions)
    transactions = trxn_filter.qs
    records = transactions

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for actor in transactions:
        if actor.payer == player:
            trxn_list.append([actor, 'N'])
        elif actor.payee == player:
            trxn_list.append([actor, 'Y'])
        else:
            pass
    receipts = []
    invoices = Invoice.objects.filter(payer=player)
    invoice_filter = InvoiceOwnerFilter(request.GET, queryset=invoices)

    if invoices:
        for invoice in invoices:
            voucher = invoice.receipt_set.all().last()
            receipts.append([invoice, voucher])

    payment_count = len(trxn_list)
    receipts = transactions.filter(payee=player)
    receipt_count = len(receipts)

    context = {
        'player': player,
        'payments': trxn_list,
        'payment_count': payment_count,
        'receipts': receipts,
        'receipt_count': receipt_count,
        'trxn_filter': trxn_filter,
        'page_obj': page_obj,
        'invoice_filter': invoice_filter,
        'alerts': alerts,
    }

    return render(request, 'mine_owner/accounts.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_accounts(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    trxn_list = []
    transactions = Trxns.objects.all()
    trxn_filter = TrxnFilter(request.GET, queryset=transactions)
    transactions = trxn_filter.qs
    records = trxn_filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for actor in transactions:
        if actor.payer == player:
            trxn_list.append([actor, 'N'])
        elif actor.payee == player:
            trxn_list.append([actor, 'Y'])
        else:
            pass
    receipts = []
    invoices = Invoice.objects.filter(payer=player)
    invoice_filter = InvoiceOwnerFilter(request.GET, queryset=invoices)

    if invoices:
        for invoice in invoices:
            voucher = invoice.receipt_set.all().last()
            receipts.append([invoice, voucher])

    payment_count = len(trxn_list)
    receipts = transactions.filter(payee=player)
    receipt_count = len(receipts)

    context = {
        'player': player,
        'payments': trxn_list,
        'payment_count': payment_count,
        'receipts': receipts,
        'receipt_count': receipt_count,
        'trxn_filter': trxn_filter,
        'page_obj': page_obj,
        'invoice_filter': invoice_filter,
        'alerts': alerts,
    }

    return render(request, 'services/proview/accounts.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_accounts(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = PlayerUserRelation.objects.filter(user=request.user).last().player
    trxn_list = []
    transactions = Trxns.objects.all()
    trxn_filter = TrxnFilter(request.GET, queryset=transactions)
    transactions = trxn_filter.qs
    records = trxn_filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for actor in transactions:
        if actor.payer == player:
            trxn_list.append(player, 0)
        elif actor.payee == player:
            trxn_list.append(player, 1)
        else:
            pass
    receipts = []
    invoices = Invoice.objects.filter(payer=player)
    invoice_filter = InvoiceOwnerFilter(request.GET, queryset=invoices)

    if invoices:
        for invoice in invoices:
            voucher = invoice.receipt_set.all().last()
            receipts.append(invoice, voucher)

    payment_count = len(trxn_list)
    receipts = transactions.objects.filter(payee=player)
    receipt_count = len(receipts)

    context = {
        'player': player,
        'payments': trxn_list,
        'payment_count': payment_count,
        'receipts': receipts,
        'receipt_count': receipt_count,
        'trxn_filter': trxn_filter,
        'page_obj': page_obj,
        'invoice_filter': invoice_filter,
        'alerts': alerts,
    }

    return render(request, 'investor/investview/trxn/lists.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_owner_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = MineOwnerRelation.objects.all()
    filter = MineOwnerFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }

    return render(request, 'mine_owner/list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_view_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = request.user.playeruserrelation_set.all().last()
    records = MineOwnerRelation.objects.filter(owner=player)
    filter = MineOwnerFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }

    return render(request, 'mine_owner/list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def service_provider_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = ServiceProv.objects.all()
    filter = ServiceProvFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }

    return render(request, 'services/provider_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mand_req_invoice_create(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mandate_request = MandateRequest.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')
    proforma = mandate_request.mandateproforma_set.all().last()
    invoice = 0
    post = None
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        form1 = TrxnForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mandate_request_id = mandate_request.id
            record.amount = proforma.amount
            record.status = "Paid"
            record.payer_id = mandate_request.cart_mine_match.cart_request.investor.player.id
            if Invoice.objects.filter(mandate_request_id=mandate_request.id).exists():
                messages.info(request, str(mandate_request)+' Invoice already exists')
                context = {
                    'form': form,
                    'form1': form1,
                    'mandate_request': mandate_request,
                    'cancel': cancel,
                    'alerts': alerts,
                }
                return render(request, 'mine_new.html', context)
            record.date_created = Now()
            record.author = request.user
            record.save()

            invoice = Invoice.objects.filter(mandate_request=mandate_request).last()
            if form1.is_valid():
                form1 = form1.save(commit=False)
                form1.invoice_ref = invoice.id
                form1.purpose = record.purpose
                form1.amount = record.amount
                form1.payee_id = mandate_request.cart_mine_match.cart_request.investor.player.id
                form1.payer_id = mandate_request.cart_mine_match.cart_request.investor.player.id
                form1.date_created = Now()
                form1.author = request.user
                form1.save()

                item = mandate_request.mandateproforma_set.all().last()
                post = get_object_or_404(MandateProforma, pk=item.id)
                form2 = TrxnMandateProForm(request.POST, instance=post)
                if form2.is_valid():
                    form2 = form2.save(commit=False)
                    form2.status = 'Confirmed'
                    form2.save()

                return redirect('investview_mandate_request.html', pk=mandate_request.id)

    form = InvoiceForm()
    form1 = TrxnForm()
    form2 = TrxnMandateProForm(instance=post)

    context = {
        'form': form,
        'form1': form1,
        'form2': form2,
        'mandate_request': mandate_request,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'mand_req_invoice_create.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def invoice_detail(request, pk, template):

    invoice = Invoice.objects.get(id=pk)

    context = {
        'invoice': invoice,
    }

    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def field_proforma_detail(request, pk):

    proforma = FieldProforma.objects.get(id=pk)
    investor = proforma.field_request.mandate.mandate_request.cart_mine_match.cart_request.investor
    support_costs = proforma.field_request.fieldsupcosts_set.all()
    services = proforma.field_request.serviceprovrequired_set.all()
    service_costs = []
    if services:
        for service in services:
            quotations = service.fieldproviderquote_set.all()
            if quotations:
                for quote in quotations:
                    if quote.fieldreqwinqte_set.all():
                        service_costs.append(quote)

    context = {
        'proforma': proforma,
        'investor': investor,
        'service_costs': service_costs,
        'support_costs': support_costs,
    }

    return render(request, 'investor/proforma_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def receipt_detail(request, pk):

    receipt = Receipt.objects.get(id=pk)

    context = {
        'receipt': receipt,
    }

    return render(request, 'receipt_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def trxn_detail(request, pk, template):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')
    trxn = Trxns.objects.get(id=pk)
    reverse_status: bool = False
    invoice = 0
    if Trxns.objects.filter(reverse_trxn=trxn.id).exists():
        reverse_status = True
    if trxn.purpose in ['Mandate Invoice', 'Field Invoice', 'Subs']:
        invoice = Invoice.objects.get(id=trxn.invoice_ref)

    context = {
        'trxn': trxn,
        'invoice': invoice,
        'reverse_status': reverse_status,
        'alerts': alerts,
        'cancel': cancel,
    }

    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def trxn_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = Trxns.objects.all()
    filter = TrxnsFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }

    return render(request, 'trxn_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investorview_trxn_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = request.user.playeruserrelation_set.all().last().player
    trxns = Trxns.objects.filter(Q(payer=player) | Q(payee=player))
    filter = TrxFilter(request.GET, queryset=trxns)
    trxns = filter.qs
    records = trxns

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'page_obj': page_obj,
        'player': player,
        'trxn_list': trxn_list,
        'alerts': alerts,
    }

    return render(request, 'investor/investview/trxn/nav_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def player_detail_template(request, pk, template_name):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = Player.objects.get(id=pk)
    indi = 0
    corp = 0
    synd = 0
    investor_status = 'Not Investor'
    if player.type == 'Individual':
        indi = IndRecord.objects.get(id=player.ref)
    elif player.type == 'Corporate':
        corp = CorpRecord.objects.get(id=player.ref)
    else:
        synd = Syndicate.objects.get(id=player.ref)

    mines = MineOwnerRelation.objects.filter(owner=player)
    mine_filter = PlayerMineFilter(request.GET, queryset=mines)
    mine_count = len(mines)
    investments = Investor.objects.filter(player=player).last()
    if investments:
        investor_status = 'Investor'

    investor = player.investor_set.all().last()
    carts = CartRequest.objects.filter(investor_id=investor.id)
    cart_filter = CartRequestFilter(request.GET, queryset=carts)
    carts = cart_filter.qs
    services = ServiceProv.objects.filter(name=player)
    service_count = len(services)
    trxn_list = []
    transactions = Trxns.objects.all()
    trxn_filter = TrxnFilter(request.GET, queryset=transactions)
    transactions = trxn_filter.qs
    for actor in transactions:
        if actor.payer == player:
            trxn_list.append([player, '0'])
        elif actor.payee == player:
            trxn_list.append([player, '1'])
        else:
            pass
    receipts = []
    item = 0
    invoices = Invoice.objects.filter(payer=player)
    invoice_filter = InvoiceOwnerFilter(request.GET, queryset=invoices)
    if invoices:
        for invoice in invoices:
            item = invoice.receipt_set.all().last()
            receipts.append([invoice, item])

    payment_count = len(trxn_list)
    receipts_list = []
    receipt_count = len(receipts_list)
    for transact in Trxns.objects.filter(payer=player):
        receipt = Receipt.objects.filter(trxn_ref=transact).last()
        receipts_list.append(receipt)

    context = {
        'player': player,
        'mines': mines,
        'mine_filter': mine_filter,
        'mine_count': mine_count,
        'investments': investments,
        'services': services,
        'service_count': service_count,
        'payments': trxn_list,
        'payment_count': payment_count,
        'receipts': receipts,
        'receipt_count': receipt_count,
        'investor_status': investor_status,
        'carts': carts,
        'cart_filter': cart_filter,
        'trxn_filter': trxn_filter,
        'invoice_filter': invoice_filter,
        'indi': indi,
        'corp': corp,
        'synd': synd,
        'alerts': alerts,
    }
    return render(request, template_name, context)


# @login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def player_detail(request, pk, template):

    player = Player.objects.get(id=pk)
    alerts = Alerts.objects.filter(player=player)
    indi = 0
    corp = 0
    synd = 0
    investor_status = 'Not Investor'
    if player.type == 'Individual':
        indi = IndRecord.objects.get(id=player.ref)
    elif player.type == 'Corporate':
        corp = CorpRecord.objects.get(id=player.ref)
    else:
        synd = Syndicate.objects.get(id=player.ref)

    mines = MineOwnerRelation.objects.filter(owner_id=player.id)
    mine_filter = PlayerMineFilter(request.GET, queryset=mines)
    mine_count = len(mines)
    mines = mine_filter.qs
    min_locs = []
    for mine in mines:
        minloc = MineLocation.objects.filter(name_id=mine.mine.id).last()
        min_locs.append(minloc)
    investments = Investor.objects.filter(player=player).last()
    if investments:
        investor_status = 'Investor'

    investor = player.investor_set.all().last()
    carts = None
    cart_filter = None
    if PlayerUserRelation.objects.filter(player=player, investor=True):
        carts = CartRequest.objects.filter(investor_id=investor.id)
        cart_filter = CartRequestFilter(request.GET, queryset=carts)
        carts = cart_filter.qs
    providers = ServiceProv.objects.filter(name_id=player.id)
    provider = None
    quotations = None
    if providers:
        provider = ServiceProv.objects.filter(name_id=player.id).last()
        quotations = FieldProviderQuote.objects.filter(provider_id=provider.id)
    service_count = len(providers)
    trxn_list = []
    transactions = Trxns.objects.all()
    trxn_filter = TrxnFilter(request.GET, queryset=transactions)
    transactions = trxn_filter.qs
    for actor in transactions:
        if actor.payer == player:
            trxn_list.append(actor)
        elif actor.payee == player:
            trxn_list.append(actor)
        else:
            pass
    receipts = []
    item = 0
    invoices = Invoice.objects.filter(payer=player)
    invoice_filter = InvoiceOwnerFilter(request.GET, queryset=invoices)
    if invoices:
        for invoice in invoices:
            item = invoice.receipt_set.all().last()
            receipts.append([invoice, item])

    payment_count = len(trxn_list)
    receipts_list = []
    receipt_count = len(receipts_list)
    for transact in Trxns.objects.filter(payer=player):
        receipt = Receipt.objects.filter(trxn_ref=transact).last()
        receipts_list.append(receipt)

    context = {
        'player': player,
        'mines': mines,
        'mine_filter': mine_filter,
        'mine_count': mine_count,
        'min_locs': min_locs,
        'investments': investments,
        'services': providers,
        'service_count': service_count,
        'payments': trxn_list,
        'payment_count': payment_count,
        'receipts': receipts,
        'receipt_count': receipt_count,
        'investor_status': investor_status,
        'carts': carts,
        'cart_filter': cart_filter,
        'trxn_filter': trxn_filter,
        'invoice_filter': invoice_filter,
        'indi': indi,
        'corp': corp,
        'synd': synd,
        'alerts': alerts,
        'quotations': quotations,
    }
    return render(request, template, context)

@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def player_detail_service(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    player = Player.objects.get(id=pk)
    indi = 0
    corp = 0
    synd = 0
    if player.type == 'Individual':
        indi = IndRecord.objects.get(id=player.ref)
    elif player.type == 'Corporate':
        corp = CorpRecord.objects.get(id=player.ref)
    else:
        synd = Syndicate.objects.get(id=player.ref)

    mines = MineOwnerRelation.objects.filter(owner=player)
    mine_filter = PlayerMineFilter(request.GET, queryset=mines)
    mine_count = len(mines)
    investments = Investor.objects.filter(player=player).last()
    investor_status = 'Not Investor'
    if investments:
        investor_status = 'Investor'

    investor = player.investor_set.all().last()
    carts = CartRequest.objects.filter(investor_id=investor.id)
    cart_filter = CartRequestFilter(request.GET, queryset=carts)
    carts = cart_filter.qs
    providers = ServiceProv.objects.filter(name_id=player.id)
    provider = ServiceProv.objects.filter(name_id=player.id).last()
    quotations = FieldProviderQuote.objects.filter(provider_id=provider.id)
    service_count = len(providers)
    trxn_list = []
    transactions = Trxns.objects.all()
    trxn_filter = TrxnFilter(request.GET, queryset=transactions)
    transactions = trxn_filter.qs
    for actor in transactions:
        if actor.payer == player:
            trxn_list.append([actor, '0'])
        elif actor.payee == player:
            trxn_list.append([actor, '1'])
        else:
            pass
    receipts = []
    item = 0
    invoices = Invoice.objects.filter(payer=player)
    invoice_filter = InvoiceOwnerFilter(request.GET, queryset=invoices)
    if invoices:
        for invoice in invoices:
            item = invoice.receipt_set.all().last()
            receipts.append([invoice, item])

    payment_count = len(trxn_list)
    receipts_list = []
    receipt_count = len(receipts_list)
    for transact in Trxns.objects.filter(payer=player):
        receipt = Receipt.objects.filter(trxn_ref=transact).last()
        receipts_list.append(receipt)

    context = {
        'player': player,
        'mines': mines,
        'mine_filter': mine_filter,
        'mine_count': mine_count,
        'investments': investments,
        'services': providers,
        'service_count': service_count,
        'payments': trxn_list,
        'payment_count': payment_count,
        'receipts': receipts,
        'receipt_count': receipt_count,
        'investor_status': investor_status,
        'carts': carts,
        'cart_filter': cart_filter,
        'trxn_filter': trxn_filter,
        'invoice_filter': invoice_filter,
        'indi': indi,
        'corp': corp,
        'synd': synd,
        'alerts': alerts,
        'quotations': quotations,
    }
    return render(request, 'player_detail_service.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def player_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    players = Player.objects.all()
    player_filter = PlayerFilter(request.GET, queryset=players)
    players = player_filter.qs
    total_list = []
    player_list = []
    records = total_list

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for player in players:
        player_list.append(player)
        if Investor.objects.filter(player=player).exists():
            player_list.append('yes')
        else:
            player_list.append('no')
        if ServiceProv.objects.filter(name=player).exists():
            player_list.append('yes')
        else:
            player_list.append('no')
        if MineOwnerRelation.objects.filter(owner=player).exists():
            player_list.append('yes')
        else:
            player_list.append('no')

        total_list.append(player_list)
        player_list = []

    context = {
        'filter': player_filter,
        'total_list': total_list,
        'page_obj': page_obj,
        'alerts': alerts,
    }
    return render(request, 'player_list.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def player_archive(request, pk, template):

    player = Player.objects.filter(id=pk).last()
    alerts = Alerts.objects.filter(player=player)
    letters = None
    agreements = None
    receipts = None
    others = None
    letter_filter = None
    agreement_filter = None
    receipt_filter = None
    doc_filter = None
    records = None
    records1 = None
    records2 = None
    records3 = None
    page_obj = None
    page_obj1 = None
    page_obj2 = None
    page_obj3 = None
    if MineLetters.objects.filter(player=player):
        letters = MineLetters.objects.filter(player_id=player.id)
        letter_filter = MineviewArchiveLetterFilter(request.GET, queryset=letters)
        records = letter_filter.qs
        paginator = Paginator(records, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    if MineAgreements.objects.filter(player=player):
        agreements = MineAgreements.objects.filter(player_id=player.id)
        agreement_filter = MineviewArchiveAgreementFilter(request.GET, queryset=agreements)
        records1 = agreement_filter.qs
        paginator1 = Paginator(records1, 15)
        page_number1 = request.GET.get('page')
        page_obj1 = paginator1.get_page(page_number1)
    if MineReceipts.objects.filter(player=player):
        receipts = MineReceipts.objects.filter(player_id=player.id)
        receipt_filter = MineviewArchiveReceiptFilter(request.GET, queryset=receipts)
        records2 = receipt_filter.qs
        paginator2 = Paginator(records2, 15)
        page_number2 = request.GET.get('page')
        page_obj2 = paginator2.get_page(page_number2)
    if OtherDocs.objects.filter(player=player):
        other_docs = OtherDocs.objects.filter(player_id=player.id)
        doc_filter = MineviewArchiveOtherFilter(request.GET, queryset=other_docs)
        records3 = doc_filter.qs
        paginator3 = Paginator(records3, 15)
        page_number3 = request.GET.get('page')
        page_obj3 = paginator3.get_page(page_number3)


    context = {
        'player': player,
        'letter_filter': letter_filter,
        'receipt_filter': receipt_filter,
        'agreement_filter': agreement_filter,
        'doc_filter': doc_filter,
        'template': template,
        'page_obj': page_obj,
        'page_obj1': page_obj1,
        'page_obj2': page_obj2,
        'page_obj3': page_obj3,
        'alerts': alerts,
    }
    return render(request, template, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def service(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    service = ServiceProv.objects.get(id=pk)
    activities = service.field_set.all()
    activity_filter = ServiceFieldFilter(request.GET, queryset=activities)
    activities= activity_filter.qs
    field_count = len(activities)

    context = {
        'service': service,
        'field_count': field_count,
        'activity_filter': activity_filter,
        'alerts': alerts,
    }

    return render(request, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def owner_type(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    service = ServiceProv.objects.get(id=pk)
    activities = service.field_set.all()
    activity_filter = ServiceFieldFilter(request.GET, queryset=activities)
    activities= activity_filter.qs
    field_count = len(activities)

    context = {
        'service': service,
        'field_count': field_count,
        'activity_filter': activity_filter,
        'alerts': alerts,
    }

    return render(request, context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def service_history_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    record = SerProvProfile.objects.get(id=pk)

    context = {
        'alerts': alerts,
        'record': record,
    }

    return render(request, 'services/work_history_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def proview_service_history_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    record = SerProvProfile.objects.get(id=pk)

    context = {
        'alerts': alerts,
        'record': record,
    }

    return render(request, 'services/proview/work_history_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mineview_service_history_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    record = SerProvProfile.objects.get(id=pk)

    context = {
        'alerts': alerts,
        'record': record,
    }

    return render(request, 'mine_owner/work_history_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_service_history_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    record = SerProvProfile.objects.get(id=pk)

    context = {
        'alerts': alerts,
        'record': record,
    }

    return render(request, 'investor/work_history_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def service_detail(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    service = ServiceProv.objects.get(id=pk)
    activities = service.field_set.all()
    activity_filter = ServiceFieldFilter(request.GET, queryset=activities)
    activities= activity_filter.qs
    field_count = len(activities)
    history = SerProvProfile.objects.filter(name=service)

    context = {
        'service': service,
        'field_count': field_count,
        'activity_filter': activity_filter,
        'alerts': alerts,
        'history': history,
    }

    return render(request, 'services/provider_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def investview_service_detail(request, pk):

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    provider = ServiceProv.objects.get(id=pk)
    history = SerProvProfile.objects.filter(name=provider)

    context = {
        'provider': provider,
        'alerts': alerts,
        'history': history,
    }

    return render(request, 'investor/investview/provider_detail.html', context)

    online = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=online)
    record = SerProvProfile.objects.get(id=pk)

    context = {
        'record': record,
        'alerts': alerts,
    }

    return render(request, 'services/work_history_detail.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def service_detail_activity(request, pk):

    context = {}
    service(request, pk)

    return render(request, 'services/detail_activities.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def deactivate_alert(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    post = get_object_or_404(Alerts, pk=pk)
    cancel = request.META.get('HTTP_REFERER')
    alert = Alerts.objects.get(id=pk)

    if request.method == 'POST':
        form = AlertEditForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            record.status = 'Off'
            record.save()
            return redirect('mine_owner/mandate_detail.html',  pk=alert.player.id)

    else:
        form = AlertEditForm()

    context = {
        'form': form,
        'alert': alert,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'deactivate_alert.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_production(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)

    if request.method == 'POST':
        form = MineProductionForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            record.date_created = Now()
            record.author = request.user
            record.save()
            return redirect('mine_detail_mine.html', pk=mine.id)

    else:
        form = MineProductionForm()

    context = {
        'form': form,
        'mine': mine,
        'alerts': alerts,
    }
    return render(request, 'mine_production.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_works(request, pk):

    mine = Mine.objects.get(id=pk)
    player = MineOwnerRelation.objects.filter(mine_id=mine.id).last().owner
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = MineWorksForm(request.POST, player=player)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            record.date_created = Now()
            record.author = request.user
            record.save()
            return redirect(cancel)

    else:
        form = MineWorksForm()

    context = {
        'form': form,
        'mine': mine,
        'alerts': alerts,
    }
    return render(request, 'mine_works.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_labour(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    mine = Mine.objects.get(id=pk)

    if request.method == 'POST':
        form = MineLabourForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            record.date_created = Now()
            record.author = request.user
            record.save()
            return redirect('mine_detail_mine.html',  pk=mine.id)

    else:
        form = MineLabourForm()

    context = {
        'form': form,
        'mine': mine,
        'alerts': alerts,
    }
    return render(request, 'mine_labour.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_plant(request, pk):

    mine = Mine.objects.get(id=pk)
    player = MineOwnerRelation.objects.filter(mine_id=mine.id).last().owner
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = MinePlantForm(request.POST, player=player)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            record.date_created = Now()
            record.author = request.user
            record.save()
            return redirect(cancel)

    else:
        form = MinePlantForm()

    context = {
        'form': form,
        'mine': mine,
        'alerts': alerts,
    }
    return render(request, 'mine_plant.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def mine_yellow_plant(request, pk):

    mine = Mine.objects.get(id=pk)
    player = MineOwnerRelation.objects.filter(mine_id=mine.id).last().owner
    alerts = Alerts.objects.filter(player=player)
    cancel = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = MineYellowPlantForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.mine_id = mine.id
            record.date_created = Now()
            record.author = request.user
            record.save()
            return redirect(cancel)

    else:
        form = MineYellowPlantForm()

    context = {
        'form': form,
        'mine': mine,
        'alerts': alerts,
    }
    return render(request, 'mine_yellow_plant.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def request_service_provider(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    post = get_object_or_404(FieldReq, id=pk)
    field_request = FieldReq.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')
    quantity = 0
    post1 = 0
    post2 = 0
    if request.method == 'POST':
        form = RequestProviderForm(request.POST, request.FILES, instance=post)
        form1 = 0
        if form.is_valid():
            obj = form.save(commit=False)
            quantity = obj.quantity
            obj.save()

            old_list = ServiceProvRequired.objects.filter(field_request_id=obj.id)
            for item in old_list:
                if item.id is request.POST.getlist('route'):
                    if  item.quantity == obj.quantity:
                        pass
                    else:
                        post1 = get_object_or_404(ServiceProvRequired, id=item.id)
                        form1 = SPReqForm(request.POST, instance=post1)
                        if form1.is_valid():
                            form1 = form1.save(commit=False)
                            form1.quantity = quantity
                            form1.save()
                            return redirect('investor/investview/fieldreq/field_activity'.html, pk=field_request.id)
                else:
                    ServiceProvRequired.objects.create(field_request_id=obj.id, provider_role_id=obj.provider_role_id, quantity=quantity)

                    return redirect('investor/investview/fieldreq/field_activity'.html, pk=field_request.id)

    else:
        form = RequestProviderForm(instance=post)

    context = {
        'form': form,
        'field_request': field_request,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'investor/request_service_provider.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def request_service_done(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    post = get_object_or_404(FieldReq, pk=pk)
    field_request = FieldReq.objects.get(id=pk)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form2 = FieldReqStatForm(request.POST, instance=post)
        if form2.is_valid():
            form2 = form2.save(commit=False)
            form2.status = 'Service Choice'
            form2.save()

            return redirect('investor/investview/fieldreq/field_activity.html', pk=field_request.id)

    else:
        form2 = FieldReqStatForm(instance=post)

    context = {
        'form2': form2,
        'field_request': field_request,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'investor/request_service_done.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def cash_in(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = Player.objects.get(pk=pk)
    post = get_object_or_404(Player, pk=pk)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CashInForm(request.POST)
        form1 = PlayerTrxnForm(request.POST, instance=post)
        form2 = TrxnForm(request.POST, instance=post)
        if form.is_valid():
            record = form.save(commit=False)
            record.player_id = player.id
            record.type = 'In'
            record.date_created = Now()
            record.author = request.user
            record.save()

            if form1.is_valid():
                form1 = form1.save(commit=False)
                form1.trxn_balance = form1.trxn_balance + record.amount
                form1.save()

                if form2.is_valid():
                    form2 = form2.save(commit=False)
                    form2.payer_id = player.id
                    form2.payee_id = player.id
                    form2.amount = record.amount
                    form2.purpose_id = 5
                    form2.date_created = Now()
                    form2.author = request.user
                    form2.save()

                    return redirect(cancel)


    else:
        form = CashInForm()
        form1 = PlayerTrxnForm(instance=post)
        form2 = TrxnForm()

    context = {
        'form': form,
        'form1': form1,
        'form2': form2,
        'player': player,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'cash_in.html', context)


@login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def cash_out(request, pk):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    player = Player.objects.get(pk=pk)
    post = get_object_or_404(Player, pk=pk)
    cancel = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CashInForm(request.POST)
        form1 = PlayerTrxnForm(request.POST, instance=post)
        form2 = TrxnForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.player_id = player.id
            record.type = 'Out'
            record = form.save(commit=False)
            if record.amount > player.trxn_balance:
                messages.info(request, 'Insufficient Balance')
                return redirect(cancel)

            record.date_created = Now()
            record.author = request.user
            record.save()

            if form1.is_valid():
                form1 = form1.save(commit=False)
                form1.trxn_balance = form1.trxn_balance - record.amount
                form1.save()

                if form2.is_valid():
                    form2 = form2.save(commit=False)
                    form2.payer_id = player.id
                    form2.payee_id = player.id
                    form2.amount = record.amount
                    form2.purpose_id = 6
                    form2.date_created = Now()
                    form2.author = request.user
                    form2.save()

                    return redirect(cancel)

    else:
        form = CashInForm()
        form1 = PlayerTrxnForm(instance=post)
        form2 = TrxnForm()

    context = {
        'form': form,
        'form1': form1,
        'form2': form2,
        'player': player,
        'cancel': cancel,
        'alerts': alerts,
    }
    return render(request, 'cash_out.html', context)


# @login_required(login_url='login.html')
# @allowed_users(allowed_roles=['admin', 'corporate_principal', 'delivery_request', 'delivery_initiator', 'accounts_changes', 'trip_originator'])
def cash_list(request):

    player = PlayerUserRelation.objects.filter(party=request.user).last().player
    alerts = Alerts.objects.filter(player=player)
    records = PlayerCash.objects.all()
    filter = CashFilter(request.GET, queryset=records)
    records = filter.qs

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': filter,
        'alerts': alerts,
        'page_obj': page_obj,
    }
    return render(request, 'cash_list.html', context)


# class MapView(TemplateView):
#     template_name = 'investor/investview/cart/lists.html'
#
#     def get_context(self, **kwargs):
#         context = {'form': CartRequestForm()}
#         return context
