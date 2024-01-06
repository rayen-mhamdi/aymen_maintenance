from django.shortcuts import render
from .models import Recu
# Create your views here.

def print_view(request, id):
  data = Recu.objects.get(id=id)
  return render(request, 'ticket.html', {"data" : data})