from django.contrib import admin
from django.http import FileResponse
from .models import *
from .actions import generate_pdf
from django.urls import reverse 
from django.http import HttpResponseRedirect 
# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ["id", "nom", "phone", "adresse",]
    list_display = ("id", "nom", "phone", "adresse",)

@admin.register(Objet)
class ObjetAdmin(admin.ModelAdmin):
    search_fields = ["nom",]
    list_display = ("nom",)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    search_fields = ["nom", "objet__nom",]
    list_display = ("nom", "nom_objet",)
    autocomplete_fields = ["objet"]
    def nom_objet(self, obj):
        return obj.objet.nom

@admin.register(Represantant)
class RepresantantAdmin(admin.ModelAdmin):
    search_fields = ["nom", "actif",]
    list_display = ("nom", "actif",)


@admin.register(Recu)
class RecuAdmin(admin.ModelAdmin):
    autocomplete_fields = ["client", "objet", "categorie", "represantant"]
    search_fields = ["id", "client__nom", "objet__nom", "categorie__nom", "marque", "status", "modifie_a"]
    list_display = ("id", "nom_client","phone", "item", "status", "prix_et_reste", "observation", "cree_a", "modifie_a")
    list_per_page = 20
    actions = ["print_action"]
    list_filter = ["status", "modifie_a", "categorie"]

    def nom_client(self, obj):
        return obj.client.nom
    
    def prix_et_reste(self, obj):
        return "{} (reste: {}) ".format(obj.prix, obj.prix-obj.accompte)
    

    def item(self, obj):
        return "{} ({}) -- {}".format(obj.objet.nom, obj.categorie.nom, obj.marque)
    
    def phone(self, obj):
        return obj.client.phone

    @admin.action(description='Imprimé Récu')
    def print_action(self, request, queryset):
        return HttpResponseRedirect(reverse('tickets:print', args=(queryset[0].id,))) #args is mandatory if the route have paramaters
