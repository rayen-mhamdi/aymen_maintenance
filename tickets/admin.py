from django.contrib import admin
from .models import *
from django.urls import reverse 
from django.http import HttpResponseRedirect 
from django.forms import TextInput, Textarea, Select
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.

class ActiveUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', )
    ordering = ('username',)
    

admin.site.unregister(User)
admin.site.register(User, ActiveUserAdmin)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ["id", "nom", "phone", "adresse",]
    list_display = ("id", "nom", "phone", "adresse",)

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
class RecuAdmin(SimpleHistoryAdmin):
    autocomplete_fields = ["client", "categorie", "objet", "status",]
    search_fields = ["id", "client__nom", "categorie__famille__nom",  "categorie__nom", "objet__nom", "marque", "status__label", "modifie_a"]
    list_display = ("id", "nom_client","phone", "item", "status_label", "prix_et_reste", "observation", "cree_a", "modifie_a")
    list_per_page = 20
    actions = ["print_action"]
    list_filter = ["categorie__famille", "categorie", "status", "modifie_a"]
    history_list_display = ("prix", "accompte", "status", "observation", "represantant")

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':80})},
        #models.ForeignKey: {'widget': Select(attrs={'style': 'width:30rem;'})},
    }
   
    def nom_client(self, obj):
        return obj.client.nom
    
    def prix_et_reste(self, obj):
        return "{} (reste: {}) ".format(obj.prix, obj.prix-obj.accompte)
    

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
        form.base_fields['represantant'].queryset = User.objects.filter(is_active=True)
        return form
    
    def get_changeform_initial_data(self, request):
        initial = super(RecuAdmin, self).get_changeform_initial_data(request)
        initial['represantant'] =  request.user
        # Get the status object that has par_default set to True
        default_status = Status.objects.filter(par_default=True).first()

        # If such a status exists, set initial['status'] to it
        if default_status is not None:
            initial['status'] = default_status

        return initial
        
    # class Media:
    #       js = ('js/recu_admin.js',)
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
            "js/admin_addon.js",
            )
