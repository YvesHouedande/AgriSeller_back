from django.db import models
import uuid
from django.core.validators import MinValueValidator
from core.localisation.models import Region
from core.producteurs.models import ProducteurPersonnePhysique, ProducteurOrganisation

class BaseModel(models.Model):
    """Classe abstraite de base pour les modèles"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_maj = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class CategorieCulture(BaseModel):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Pour icônes FontAwesome

    class Meta:
        verbose_name = "Catégorie de culture"
        verbose_name_plural = "Catégories de cultures"
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Culture(BaseModel):
    class SaisonPlantation(models.TextChoices):
        SECHE = 'saison_seche', 'Saison sèche'
        PLUIES = 'saison_pluies', 'Saison des pluies'
        TOUTE_ANNEE = 'toute_annee', 'Toute l\'année'

    class DureeCycle(models.TextChoices):
        COURTE = 'courte', 'Courte (<3 mois)'
        MOYENNE = 'moyenne', 'Moyenne (3-6 mois)'
        LONGUE = 'longue', 'Longue (>6 mois)'

    nom = models.CharField(max_length=200)
    nom_scientifique = models.CharField(max_length=200, blank=True)
    categorie = models.ForeignKey(CategorieCulture, on_delete=models.PROTECT)
    regions = models.ManyToManyField(Region, related_name='cultures')
    saison_plantation = models.CharField(max_length=20, choices=SaisonPlantation.choices)
    duree_cycle = models.CharField(max_length=10, choices=DureeCycle.choices)
    duree_cycle_jours = models.PositiveIntegerField()
    image = models.ImageField(upload_to='cultures/', blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Culture"
        verbose_name_plural = "Cultures"
        ordering = ['nom']
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['categorie']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.categorie})"

class ExploitationAgricole(BaseModel):
    class StatutExploitation(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        PREPARATION = 'en_preparation', 'En préparation'

    class TypePropriete(models.TextChoices):
        PROPRIETE = 'propriete', 'Propriété'
        LOCATION = 'location', 'Location'
        METAYAGE = 'metayage', 'Métayage'

    producteur_physique = models.ForeignKey(
        ProducteurPersonnePhysique,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='exploitations_physique'
    )
    producteur_organisation = models.ForeignKey(
        ProducteurOrganisation,
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
        related_name='exploitations_organisation'
    )
    nom = models.CharField(max_length=200)
    superficie = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.1)]
    )
    adresse = models.CharField(max_length=200)
    coordonnees_gps = models.CharField(max_length=100, blank=True)
    type_propriete = models.CharField(max_length=20, choices=TypePropriete.choices)
    statut = models.CharField(max_length=20, choices=StatutExploitation.choices, default='active')
    photo = models.ImageField(upload_to='exploitations/', blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Exploitation Agricole"
        verbose_name_plural = "Exploitations Agricoles"
        ordering = ['-date_creation']
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    producteur_physique__isnull=False) | 
                    models.Q(producteur_organisation__isnull=False),
                name='producteur_required'
            )
        ]

    @property
    def producteur(self):
        return self.producteur_physique or self.producteur_organisation

    def __str__(self):
        return f"{self.nom} ({self.producteur})"

class ExploitationCulture(BaseModel):
    class MethodeCulture(models.TextChoices):
        TRADITIONNELLE = 'traditionnel', 'Traditionnelle'
        MODERNE = 'moderne', 'Moderne'
        BIO = 'bio', 'Biologique'

    exploitation = models.ForeignKey(ExploitationAgricole, on_delete=models.CASCADE, related_name='cultures_plantees')
    culture = models.ForeignKey(Culture, on_delete=models.PROTECT)
    methode = models.CharField(max_length=20, choices=MethodeCulture.choices)
    superficie_allouee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    varietes = models.TextField(blank=True)
    techniques = models.TextField(blank=True)
    date_plantation = models.DateField(null=True, blank=True)
    date_recolte_prevue = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Culture d'exploitation"
        verbose_name_plural = "Cultures d'exploitation"
        unique_together = ['exploitation', 'culture']
        ordering = ['-date_plantation']

    def __str__(self):
        return f"{self.culture.nom} ({self.superficie_allouee} ha) - {self.exploitation.nom}"