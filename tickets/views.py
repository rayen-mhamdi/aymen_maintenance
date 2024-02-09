from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.utils import timezone
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
# Create your views here.

@login_required
def print_view(request, id):
  data = Recu.objects.get(id=id)
  return render(request, 'ticket.html', {"data" : data})



@login_required
def home(request):

  # Get today's date
  today = timezone.now().date()

  # Count of Recu where cree_a is today
  today_count = Recu.objects.filter(cree_a__date=today).count()
  # Calculate the start of the current week
  current_week_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
  current_week_start -= timedelta(days=current_week_start.weekday())

  # Count of Recu where cree_a is in this week
  week_count = Recu.objects.annotate(year=ExtractYear('cree_a'), month=ExtractMonth('cree_a'), day=ExtractDay('cree_a')).filter(year=current_week_start.year, month=current_week_start.month, day__gte=current_week_start.day).count()

  # Calculate the start of the current month
  current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

  # Count of Recu where cree_a is in this month
  month_count = Recu.objects.annotate(year=ExtractYear('cree_a'), month=ExtractMonth('cree_a'), day=ExtractDay('cree_a')).filter(year=current_month_start.year, month=current_month_start.month, day__gte=current_month_start.day).count()

  data = {
    "today_count" : today_count,
    "week_count" : week_count,
    "month_count" : month_count,
    "global" : {
      "clients" : Client.objects.all().count(),
      "recus" : Recu.objects.all().count(),
      "users" : User.objects.all().count(),
    }
  }
  return render(request, 'home.html', data)


@login_required
def find_ticket(request):
  id_recu = request.POST.get('id_recu')
  return HttpResponseRedirect(reverse('tickets:display_ticket', args=(id_recu,))) #args is mandatory if the route have paramaters


def display_ticket(request, id):
  recu = Recu.objects.filter(id=id).first()

  data = {
    "id" : id,
    "recu" : recu
  }

  return render(request, 'display.html', data)