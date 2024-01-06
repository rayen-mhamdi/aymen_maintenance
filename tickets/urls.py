#in urls.py of the application

from django.urls import path

from . import views

app_name = "tickets"
urlpatterns = [
  path('print/<int:id>/', views.print_view, name="print"),
]