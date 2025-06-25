from django.db import models
import uuid
from core.localisation.models import Region
from core.producteurs.models import ProducteurPersonnePhysique, ProducteurOrganisation

class CategorieCulture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Catégorie de culture"
        verbose_name_plural = "Catégories de cultures"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class Culture(models.Model):
    SAISONS = [
        ('saison_seche', 'Saison sèche'),
        ('saison_pluies', 'Saison des pluies'), 
        ('toute_annee', 'Toute l\'année'),
    ]
    
    DUREES_CYCLE = [
        ('courte', 'Courte (<3 mois)'),
        ('moyenne', 'Moyenne (3-6 mois)'),
        ('longue', 'Longue (>6 mois)'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=200)
    nom_scientifique = models.CharField(max_length=200, blank=True)
    categorie = models.ForeignKey(CategorieCulture, on_delete=models.CASCADE)
    regions = models.ManyToManyField(Region, related_name='cultures')
    
    # Caractéristiques
    saison_plantation = models.CharField(max_length=20, choices=SAISONS)
    duree_cycle = models.CharField(max_length=10, choices=DUREES_CYCLE)
    duree_cycle_jours = models.PositiveIntegerField()
    
    # Visuel
    image = models.ImageField(upload_to='cultures/', blank=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Culture"
        verbose_name_plural = "Cultures"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.categorie})"

class ExploitationAgricole(models.Model):
    STATUTS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('en_preparation', 'En préparation'),
    ]
    
    TYPES_PROPRIETE = [
        ('propriete', 'Propriété'),
        ('location', 'Location'),
        ('metayage', 'Métayage'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relations polymorphiques avec les producteurs
    producteur_physique = models.ForeignKey(
        ProducteurPersonnePhysique,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='exploitation_physique'
    )
    producteur_organisation = models.ForeignKey(
        ProducteurOrganisation,
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
        related_name='exploitation_organisation'
    )
    
    # Identification
    nom = models.CharField(max_length=200)
    superficie = models.DecimalField(max_digits=10, decimal_places=2, help_text="Superficie en hectares")
    
    # Localisation
    adresse = models.CharField(max_length=200)
    coordonnees_gps = models.CharField(max_length=100, blank=True)
    
    # Statut
    type_propriete = models.CharField(max_length=20, choices=TYPES_PROPRIETE)
    statut = models.CharField(max_length=20, choices=STATUTS, default='active')
    date_creation = models.DateField(null=True, blank=True)
    
    # Documents
    photo = models.ImageField(upload_to='exploitations/', blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Exploitation Agricole"
        verbose_name_plural = "Exploitations Agricoles"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.producteur})"

class ExploitationCulture(models.Model):
    METHODES = [
        ('traditionnel', 'Traditionnelle'),
        ('moderne', 'Moderne'),
        ('bio', 'Biologique'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exploitation = models.ForeignKey(ExploitationAgricole, on_delete=models.CASCADE, related_name='cultures')
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    
    # Détails culturaux
    methode = models.CharField(max_length=20, choices=METHODES)
    superficie_allouee = models.DecimalField(max_digits=6, decimal_places=2)
    varietes = models.TextField(blank=True)
    techniques = models.TextField(blank=True)
    
    # Suivi
    date_plantation = models.DateField(null=True, blank=True)
    date_recolte_prevue = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Culture d'exploitation"
        verbose_name_plural = "Cultures d'exploitation"
        unique_together = ['exploitation', 'culture']
    
    def __str__(self):
        return f"{self.culture.nom} @ {self.exploitation.nom}"