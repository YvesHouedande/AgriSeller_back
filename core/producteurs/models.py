from django.db import models
import uuid
from django.core.validators import RegexValidator
from core.accounts.models import User
from core.localisation.models import Ville, Region, Pays 

class BaseProducteur(models.Model):
    """Modèle abstrait de base pour tous les types de producteurs"""
    CERTIFICATIONS = [
        ('bio', 'Agriculture biologique'),
        ('raisonnee', 'Agriculture raisonnée'),
        ('conventionnelle', 'Agriculture conventionnelle'),
        ('permaculture', 'Permaculture'),
    ]
    
    # Champs communs
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Informations professionnelles
    experience_agricole = models.PositiveIntegerField(
        default=0,
        help_text="Années d'expérience"
    )
    certification = models.CharField(
        max_length=20, 
        choices=CERTIFICATIONS, 
        blank=True
    )
    
    # Contact et réseaux
    telephone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?[0-9]{9,15}$')],
        blank=True
    )
    site_web = models.URLField(blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    whatsapp = models.CharField(max_length=15, blank=True)
    
    # Localisation
    adresse = models.CharField(max_length=200)
    ville = models.ForeignKey(Ville, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    pays = models.ForeignKey(Pays, on_delete=models.SET_NULL, null=True)
    
    # Statut
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        verbose_name = "Producteur"
        verbose_name_plural = "Producteurs"
    
    def __str__(self):
        return self.user.get_full_name()

class ProducteurPersonnePhysique(BaseProducteur):
    """Producteur individuel (personne physique)"""
    # Informations personnelles
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=200, blank=True)
    numero_cni = models.CharField(
        max_length=50, 
        blank=True,
        verbose_name="Numéro CNI"
    )
    
    # Situation familiale
    situation_matrimoniale = models.CharField(
        max_length=20,
        choices=[
            ('celibataire', 'Célibataire'),
            ('marie', 'Marié(e)'),
            ('divorce', 'Divorcé(e)'),
            ('veuf', 'Veuf/Veuve'),
        ],
        blank=True
    )
    nombre_enfants = models.PositiveIntegerField(default=0)
    
    # Contact d'urgence
    contact_urgence_nom = models.CharField(max_length=200, blank=True)
    contact_urgence_telephone = models.CharField(max_length=15, blank=True)
    
    class Meta:
        verbose_name = "Producteur (Personne Physique)"
        verbose_name_plural = "Producteurs (Personnes Physiques)"
    
    def get_age(self):
        """Calcul de l'âge du producteur"""
        from datetime import date
        if self.date_naissance:
            return date.today().year - self.date_naissance.year
        return None

class ProducteurOrganisation(BaseProducteur):
    """Producteur organisation (coopérative, GIE, etc.)"""
    TYPES_ORGANISATION = [
        ('cooperative', 'Coopérative'),
        ('societe', 'Société agricole'),
        ('association', 'Association'),
        ('groupement', 'Groupement d\'intérêt économique'),
    ]
    
    # Informations légales
    raison_sociale = models.CharField(max_length=200)
    type_organisation = models.CharField(
        max_length=20,
        choices=TYPES_ORGANISATION
    )
    numero_registre = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Numéro de registre"
    )
    
    # Dirigeant
    nom_dirigeant = models.CharField(max_length=200)
    fonction_dirigeant = models.CharField(max_length=100)
    
    # Statistiques
    nombre_membres = models.PositiveIntegerField(null=True, blank=True)
    capital_social = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "Producteur (Organisation)"
        verbose_name_plural = "Producteurs (Organisations)"
    
    def __str__(self):
        return self.raison_sociale