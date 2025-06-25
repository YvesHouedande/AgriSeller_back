from django.db import models

# Create your models here.
from django.db import models
import uuid

class Pays(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, unique=True)
    code_iso = models.CharField(max_length=3, unique=True)
    
    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class Region(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Région"
        verbose_name_plural = "Régions"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.pays.nom})"

class Ville(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    code_postal = models.CharField(max_length=10, blank=True)
    
    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"
        ordering = ['nom']
        unique_together = ['nom', 'region']
    
    def __str__(self):
        return f"{self.nom} ({self.region.nom})"