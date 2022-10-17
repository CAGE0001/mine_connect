from django.conf import settings
from .models import *
from django.db.models.functions import Now
from django.utils import timezone
from datetime import timedelta, timezone, date, datetime

def schedule_subs():
    players = Player.objects.exclude(active='False')
    message = None
    due_date = None
    odd_months = [1, 3, 5, 7, 8, 10, 12]
    even_months = [4, 6, 9, 11]

    for player in players:
        due_date = player.payment_date
        message = 'Your subscriptions of $ {} are due by the {} your account balance is $ {}'.format(player.sub_amount, player.payment_date, player.trxn_balance)
        def alert():
            if due_date.month - Now.month <= 1:
                if due_date.day == Now.day:
                    Alerts.objects.create(player=player, message=message)
                if due_date.day - Now.day == 7:
                    Alerts.objects.create(player=player, message=message)
                if due_date.day - Now.day == 1:
                    Alerts.objects.create(player=player, message=message)
        if player.payment_date > Now:
            if due_date.month is odd_months and Now.month is odd_months:
                alert()
            elif due_date.month is even_months and Now.month is even_months:
                alert()
            elif due_date.month is even_months and Now.month is odd_months:
                alert()
            elif due_date.month is odd_months and Now.month is even_months:
                if Now.day == 30 and due_date.day == 31:
                    Alerts.objects.create(player=player, message=message)
                else:
                    alert()
            else:
                if Now.day == 28 and due_date.day > 28:
                    Alerts.objects.create(player=player, message=message)
                else:
                    alert()