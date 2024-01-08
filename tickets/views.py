from django.shortcuts import render
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.db.models.functions import TruncWeek, TruncMonth
from django.utils import timezone
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
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

  # Count of Recu where cree_a is in this week
  week_count = Recu.objects.annotate(week=TruncWeek('cree_a')).filter(week=TruncWeek(timezone.now())).count()

  # Count of Recu where cree_a is in this month
  month_count = Recu.objects.annotate(month=TruncMonth('cree_a')).filter(month=TruncMonth(timezone.now())).count()

  total_count = Recu.objects.all().count()

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