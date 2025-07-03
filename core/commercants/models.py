# from django.db import models
# import uuid
# from core.accounts.models import User
# from core.localisation.models import Ville
# from django.core.validators import RegexValidator 

# class Acheteur(models.Model):
#     TYPES_COMMERCANT = [
#         ('DETAIL', 'Détaillant'),
#         ('GROS', 'Grossiste'),
#         ('EXPORT', 'Exportateur'),
#         ('IMPORT', 'Importateur'),
#     ]
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='commercant')
#     type_commercant = models.CharField(max_length=10, choices=TYPES_COMMERCANT)
#     raison_sociale = models.CharField(max_length=200, blank=True, null=True)
#     numero_registre = models.CharField(max_length=50, blank=True)
#     adresse = models.CharField(max_length=200, blank=True, null=True)
#     ville = models.ForeignKey(Ville, on_delete=models.PROTECT, null=True, blank=True, related_name='commercants')
#     numero_cni = models.CharField(max_length=20, blank=True, null=True)
#     site_web = models.URLField(blank=True)
#     actif = models.BooleanField(default=True)
#     telephone = models.CharField(
#         max_length=15,
#         validators=[RegexValidator(regex=r'^\+?[0-9]{9,15}$')],
#         blank=True
#     )

#     date_creation = models.DateTimeField(auto_now_add=True, null=True)
#     date_maj = models.DateTimeField(auto_now=True, null=True)

#     class Meta:
#         verbose_name = "Commerçant"
#         verbose_name_plural = "Commerçants"
#         ordering = ['-date_creation']

#     def __str__(self):
#         return f"{self.raison_sociale} ({self.get_type_commercant_display()})"


# core/commercants/models.py
from django.db import models
import uuid
from django.core.validators import RegexValidator
from core.localisation.models import Ville, Region, Pays 

class BaseAcheteur(models.Model):
    """Modèle abstrait de base pour tous les types d'acheteurs"""
    TYPES_COMMERCE = [
        ('DETAIL', 'Détaillant'),
        ('GROS', 'Grossiste'),
        ('EXPORT', 'Exportateur'),
        ('IMPORT', 'Importateur'),
    ]
    
    # Champs communs  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('core_accounts.User', on_delete=models.CASCADE)  
    
    # Informations professionnelles
    experience_commerciale = models.PositiveIntegerField(
        default=0,
        help_text="Années d'expérience dans le commerce"
    )
    type_commerce = models.CharField(
        max_length=20, 
        choices=TYPES_COMMERCE,
        verbose_name="Type de commerce",
        help_text="Type d'activité commerciale de l'acheteur",
        null=True,
        blank=True
    )
    
    # Contact et réseaux
    site_web = models.URLField(blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    whatsapp = models.CharField(max_length=15, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    
    # Localisation
    adresse = models.CharField(max_length=200)
    ville = models.ForeignKey(Ville, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    pays = models.ForeignKey(Pays, on_delete=models.SET_NULL, null=True)
    
    # Horaires
    horaires_ouverture = models.CharField(max_length=200, blank=True)
    
    # Statut
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        verbose_name = "Acheteur"
        verbose_name_plural = "Acheteurs"
    
    def __str__(self):
        return self.user.get_full_name()

class AcheteurPersonnePhysique(BaseAcheteur):
    """Acheteur individuel (personne physique)"""
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
    
    # Contact d'urgence
    contact_urgence_nom = models.CharField(max_length=200, blank=True)
    contact_urgence_telephone = models.CharField(max_length=15, blank=True)
    
    class Meta:
        verbose_name = "Acheteur (Personne Physique)"
        verbose_name_plural = "Acheteurs (Personnes Physiques)"
    
    def get_age(self):
        """Calcul de l'âge de l'acheteur"""
        from datetime import date
        if self.date_naissance:
            return date.today().year - self.date_naissance.year
        return None

    

class AcheteurOrganisation(BaseAcheteur):
    """Acheteur organisation (SARL, SA, GIE, etc.)"""
    FORMES_JURIDIQUES = [
        ('sarl', 'SARL'),
        ('sa', 'SA'),
        ('sasu', 'SASU'),
        ('gie', 'GIE'),
        ('cooperative', 'Coopérative'),
    ]
    
    # Informations légales
    raison_sociale = models.CharField(max_length=200)
    forme_juridique = models.CharField(
        max_length=20,
        choices=FORMES_JURIDIQUES
    )
    numero_registre = models.CharField(
        max_length=50,
        verbose_name="Numéro de registre de commerce"
    )
    date_immatriculation = models.DateField()
    
    # Dirigeant
    nom_dirigeant = models.CharField(max_length=200)
    fonction_dirigeant = models.CharField(max_length=100)
    
    # Statistiques
    nombre_employes = models.PositiveIntegerField(null=True, blank=True)
    chiffre_affaires_annuel = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Infos bancaires
    iban = models.CharField(max_length=34, blank=True)
    nom_banque = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "Acheteur (Organisation)"
        verbose_name_plural = "Acheteurs (Organisations)"
    
    def __str__(self):
        return self.raison_sociale