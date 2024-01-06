from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Client(models.Model):
    nom = models.CharField( max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=8, null=True, blank=True)
    adresse = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return "Nom: {} Phone: {} Adresse: {}".format(self.nom, self.phone, self.adresse)

class Objet(models.Model):
    nom = models.CharField(max_length=200, null=False, blank=False)
    def __str__(self):
        return self.nom

class Categorie(models.Model):
    nom = models.CharField(max_length=200, null=False, blank=False)
    objet = models.ForeignKey(Objet, on_delete=models.CASCADE, related_name="categories")
    def __str__(self):
        return self.nom

class Represantant(models.Model):
    nom = models.CharField(max_length=200, null=False, blank=False)
    actif = models.BooleanField(default=True)
    def __str__(self):
        return self.nom


class Recu(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="recus")

    objet = models.ForeignKey(Objet, on_delete=models.PROTECT, related_name="recus")
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="recus")
    marque = models.CharField(max_length=200, null=False, blank=False)

    probleme = models.CharField(max_length=200, null=False, blank=False)
    note = models.TextField(max_length=500, null=False, blank=False)
    prix = models.DecimalField(max_digits = 10, decimal_places = 3, null=False, blank=False, default=0)
    accompte = models.DecimalField(max_digits = 10, decimal_places = 3, null=False, blank=False, default=0)

    STATUS_CHOICES = [
        ('EN_COURS', 'En Cours'),

        ('REPARE', 'Réparé'),
        ('NON_REPARE', 'Non Réparé'),

        ('SORTIE_REPARE', 'Sortie Réparé'),
        ('SORTIE_NON_REPARE', 'Sortie Non Réparé'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False, blank=False, default=STATUS_CHOICES[0][0])
    observation = models.TextField(max_length=500, null=True, blank=True)

    represantant = models.ForeignKey(Represantant, on_delete=models.PROTECT, related_name="recus")

    cree_a = models.DateTimeField(auto_now_add=True)
    modifie_a = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Récu: {}".format(self.id)