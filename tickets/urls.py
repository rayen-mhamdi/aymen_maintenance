#in urls.py of the application

from django.urls import path

from . import views

app_name = "tickets"
urlpatterns = [
    path('', views.home, name="home"),
    path('find_ticket/', views.find_ticket, name="find_ticket"),
    path('display_ticket/<id>', views.display_ticket, name="display_ticket"),
    path('print/<int:id>/', views.print_view, name="print"),
]