from django.contrib import admin

from .filters import IDFilter
from .models import *
from django.urls import reverse 
from django.http import HttpResponseRedirect 
from django.forms import TextInput, Textarea, Select
from simple_history.admin import SimpleHistoryAdmin
from .utulities import ExportRecuExcelMixin
from django.contrib.admin.actions import delete_selected
from django.contrib.auth.admin import UserAdmin
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)
from django.db.models import Count, Sum

# Register your models here.

delete_selected.short_description = 'Supprimer les lignes sélectionnés'


class ActiveUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'groupe', 'is_active', 'is_superuser')
    search_fields = ('username', )
    ordering = ('username',)
    fieldsets = [
        ('Informations Additionnelles', {'fields': ["email", "is_active",  "is_superuser", "groups"]}),
        ]
    def groupe(self, obj):
        group_names = obj.groups.values_list('name', flat=True)
        group_names_str = '-'.join(map(str, group_names))
        return group_names_str
    
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        return super().save_model(request, obj, form, change)
    

admin.site.unregister(User)
admin.site.register(User, ActiveUserAdmin)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ["id", "nom", "phone", "adresse",]
    #list_display = ("id", "nom", "phone", "adresse", "chiffre_affaire", "nb_recus")
    
    # NumericRangeFilterBuilder dosent work with anotated fields
    # list_filter = [
    #     ('nb_recus', NumericRangeFilterBuilder(title="Nombre des récus",)),
    #     ('chiffre_affaire', NumericRangeFilterBuilder(title="Chiffre d'affaire",)),
    #     ]
    
    def get_list_display(self, request):
        list_display = ["id", "nom", "phone", "adresse", "nb_recus"]
        # Check if the user is authenticated and is a superuser
        if request.user.is_authenticated and request.user.is_superuser:
            list_display.append("chiffre_affaire")
        return list_display

    def chiffre_affaire(self, obj):
        return obj.recus.all().count()
    
    def nb_recus(self, obj):
        return 0
    
    nb_recus.admin_order_field = 'recus_count'  # Use the annotated field for sorting
    nb_recus.short_description = 'Nombre des Récus'

    def chiffre_affaire(self, obj):
        return 0
    
    chiffre_affaire.admin_order_field = 'total_price'  # Use the annotated field for sorting
    chiffre_affaire.short_description = "Chiffre d'affaire"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            recus_count=Count('recus'),
            total_price=Sum('recus__accompte')  # Assuming 'accompte' is the field name in 'recus' model
        )

@admin.register(Famille)
class FamilleAdmin(admin.ModelAdmin):
    search_fields = ["nom"]
    list_display = ("nom",)
    
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    search_fields = ["nom", "famille__nom",]
    list_display = ("nom", "nom_famille",)
    autocomplete_fields = ["famille"]
    def nom_famille(self, obj):
        return obj.famille.nom
    
@admin.register(Objet)
class ObjetAdmin(admin.ModelAdmin):
    search_fields = ["nom",]
    list_display = ("nom",)

# @admin.register(Represantant)
# class RepresantantAdmin(admin.ModelAdmin):
#     search_fields = ["nom", "actif",]
#     list_display = ("nom", "actif",)

#     def get_search_results(self, request, queryset, search_term):
#        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
#        return queryset.filter(actif=True).order_by('nom'), use_distinct

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ["label",]
    list_display = ("label", "par_default", )

@admin.register(Recu)
class RecuAdmin(SimpleHistoryAdmin, ExportRecuExcelMixin):
    history_list_display = ['history_date', 'history_type', 'history_user']
    exclude = ('cree_par', 'represantant',)
    autocomplete_fields = ["client", "categorie", "objet", "status",]
    search_fields = ["id", "client__nom", "categorie__famille__nom",  "categorie__nom", "objet__nom", "marque", "status__label"]
    list_display = ("id", "nom_client","phone", "item", "status_label", "prix", "accompte", "reste", "observation", 'cree_par', 'represantant', "cree_a", "modifie_a")
    readonly_fields = ['cree_par', 'represantant']
    list_per_page = 20
    actions = ["print_action", "export_as_excel"]
    list_filter = [
        IDFilter, 
        "categorie__famille", "categorie", "status", 'cree_par', 'represantant',
        ('cree_a', DateRangeFilterBuilder(title="Crée à",)),
        ('modifie_a', DateRangeFilterBuilder(title="Modifié le",)),
        
        ]
    history_list_display = ("prix", "accompte", "status","probleme", "observation", "cree_par", "represantant")

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':80})},
        #models.ForeignKey: {'widget': Select(attrs={'style': 'width:30rem;'})},
    }
   
    def nom_client(self, obj):
        return obj.client.nom
    
    def prix_et_reste(self, obj):
        return "{} (reste: {}) ".format(obj.prix, obj.prix-obj.accompte)

    def reste(self, obj):
        return obj.prix-obj.accompte
    

    def item(self, obj):
        return "{} ({}) -- {}".format(obj.objet.nom, obj.categorie.nom, obj.marque)
    
    def phone(self, obj):
        return obj.client.phone
    
    def status_label(slef, obj):
        return obj.status.label
    
    @admin.action(description='Imprimé Récu')
    def print_action(self, request, queryset):
        return HttpResponseRedirect(reverse('tickets:print', args=(queryset[0].id,))) #args is mandatory if the route have paramaters
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        #form.base_fields['represantant'].queryset = User.objects.exclude(groups__name__in=['Anonyme']).filter(is_active=True)
        return form
    
    def get_changeform_initial_data(self, request):
        initial = super(RecuAdmin, self).get_changeform_initial_data(request)

        # initial['cree_par'] = request.user
        # initial['represantant'] =  request.user

        # Get the status object that has par_default set to True
        default_status = Status.objects.filter(par_default=True).first()

        # If such a status exists, set initial['status'] to it
        if default_status is not None:
            initial['status'] = default_status

        return initial
    
    def save_model(self, request, obj, form, change):
        # Set your field here
        if not obj.pk:  # If the object is being created, not updated
            obj.cree_par = request.user
        obj.represantant = request.user
        super().save_model(request, obj, form, change)
        
    # class Media:
    #       js = ('js/recu_admin.js',)
    class Media:
        js = (
            'js/jquery.min.js',  # jquery
            "js/admin_addon.js",
            )
