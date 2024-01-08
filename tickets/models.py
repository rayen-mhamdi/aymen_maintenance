from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
# Create your models here.





class Famille(models.Model):
    nom = models.CharField(max_length=200, null=False, blank=False)
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name_plural = "1- Familles"

class Categorie(models.Model):
    nom = models.CharField(max_length=200, null=False, blank=False)
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name="categories")
    def __str__(self):
        return "{} ({})".format(self.nom, self.famille.nom)
    class Meta:
        verbose_name_plural = "2- Categories"

  
class Objet(models.Model):
    nom = models.CharField(max_length=200, null=False, blank=False)
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name_plural = "3- Objets"

class Status(models.Model):
    label = models.CharField(max_length=200, null=False, blank=False)
    par_default = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
       if self.par_default:
           Status.objects.exclude(id=self.id).update(par_default=False)
       super().save(*args, **kwargs)

    def __str__(self):
        return self.label
    
    class Meta:
       verbose_name_plural = "4- Status"
       ordering = ['id']


class Client(models.Model):
    nom = models.CharField( max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=8, null=True, blank=True)
    adresse = models.TextField(max_length=500, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank = True)

    class Meta:
       ordering = ['id']
       
    def __str__(self):
        return "Nom: {} Phone: {} Adresse: {}".format(self.nom, self.phone, self.adresse)
    
    class Meta:
        verbose_name_plural = "5- Clients"

class Recu(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="recus")
    
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="recus")
    objet = models.ForeignKey(Objet, on_delete=models.PROTECT, related_name="recus")
    marque = models.CharField(max_length=200, null=False, blank=False)
    probleme = models.CharField(max_length=200, null=False, blank=False)
    note = models.TextField(max_length=500, null=False, blank=False)
    
    prix = models.DecimalField(max_digits = 10, decimal_places = 3, null=False, blank=False, default=0)
    accompte = models.DecimalField(max_digits = 10, decimal_places = 3, null=False, blank=False, default=0)

    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="recus")
    
    observation = models.TextField(max_length=500, null=True, blank=True)

    represantant = models.ForeignKey(User, on_delete=models.PROTECT, related_name="recus")

    cree_a = models.DateTimeField(auto_now_add=True)
    modifie_a = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def get_reste(self):
        return self.prix - self.accompte
    
    def __str__(self):
        return "Récu: {}".format(self.id)
    
    class Meta:
        verbose_name_plural = "6- Récus"




# class Represantant(models.Model):
#     nom = models.CharField(max_length=200, null=False, blank=False)
#     actif = models.BooleanField(default=True)
#     def __str__(self):
#         return self.nom
