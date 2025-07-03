# accounts/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from django.core.validators import RegexValidator
from core.producteurs.models import ProducteurPersonnePhysique, ProducteurOrganisation
from core.commercants.models import AcheteurPersonnePhysique, AcheteurOrganisation 


class UserManager(BaseUserManager):
    def create_user(self, telephone, password=None, **extra_fields):
        """
        Crée et enregistre un utilisateur avec le téléphone et mot de passe.
        """
        if not telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        
        # Vérifie si le numéro existe déjà
        if self.model.objects.filter(telephone=telephone).exists():
            raise ValueError('Ce numéro de téléphone est déjà utilisé')
        
        try:
            user = self.model(
                telephone=telephone,
                **extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        except Exception as e:
            raise ValueError(f"Erreur lors de la création de l'utilisateur: {str(e)}")

    def create_superuser(self, telephone, password=None, **extra_fields):
        """
        Crée et enregistre un superutilisateur avec le téléphone et mot de passe.
        """
        try:
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_verified', True)
            extra_fields.setdefault('role', self.model.Role.ADMIN)

            return self.create_user(telephone, password, **extra_fields)
        except Exception as e:
            raise ValueError(f"Erreur lors de la création du superutilisateur: {str(e)}")

class User(AbstractUser):
    # Configuration d'authentification
    username = None
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = []  # Champs requis pour createsuperuser
    
    objects = UserManager()

    class Role(models.TextChoices):
        PRODUCTEUR = 'PROD', 'Producteur'
        COMMERCANT = 'ACHE', 'Acheteur'
        VALIDATEUR = 'VALID', 'Validateur'
        ADMIN = 'ADMIN', 'Administrateur'
    
    # Identifiant unique
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Champs obligatoires
    telephone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        unique=True,
        verbose_name='Numéro de téléphone'
    )
    role = models.CharField(
        max_length=5,
        choices=Role.choices,
        verbose_name='Rôle utilisateur'
    )
    
    # Statut et vérification
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Vérifié'
    )
    
    # Métadonnées
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )
    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière mise à jour"
    )
    
    # Fichiers
    photo_profil = models.ImageField(
        upload_to='profils/',
        blank=True,
        null=True,
        verbose_name='Photo de profil'
    )

    def __str__(self):
        name = self.get_full_name() or self.telephone
        return f"{name} ({self.get_role_display()})"

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def get_producteur(self):
        """Retourne le producteur associé à cet utilisateur s'il existe"""
        try:
            return self.producteurpersonnephysique
        except ProducteurPersonnePhysique.DoesNotExist:
            try:
                return self.producteurorganisation
            except ProducteurOrganisation.DoesNotExist:
                return None
    
    def get_producteur_type(self):
        """Retourne le type de producteur ou None"""
        if hasattr(self, 'producteurpersonnephysique'):
            return 'personne_physique'
        elif hasattr(self, 'producteurorganisation'):
            return 'organisation'
        return None


    def get_producteur_ville(self):
        """Retourne la ville associée à l'utilisateur"""
        return self.get_producteur().ville.nom if self.get_producteur() else None
    
    def get_producteur_region(self):
        """Retourne la région associée à l'utilisateur"""
        return self.get_producteur().region.nom if self.get_producteur() else None

    def get_producteur_pays(self):
        """Retourne le pays associé à l'utilisateur"""
        return self.get_producteur().pays.nom if self.get_producteur() else None

    def get_producteur_addresse(self):
        """Retourne l'adresse associée à l'utilisateur"""
        return self.get_producteur().adresse.nom if self.get_producteur() else None 

    def get_acheteur(self):
        """Retourne l'acheteur associé à cet utilisateur s'il existe"""
        try:
            return self.acheteurpersonnephysique
        except AcheteurPersonnePhysique.DoesNotExist:
            try:
                return self.acheteurorganisation
            except AcheteurOrganisation.DoesNotExist:
                return None
    
    def get_acheteur_type(self):
        """Retourne le type d'acheteur ou None"""
        if hasattr(self, 'acheteurpersonnephysique'):
            return 'personne_physique'
        elif hasattr(self, 'acheteurorganisation'):
            return 'organisation'
        return None

    def get_acheteur_ville(self):
        """Retourne la ville associée à l'acheteur"""
        return self.get_acheteur().ville.nom if self.get_acheteur() else None

    def get_acheteur_region(self):
        """Retourne la région associée à l'acheteur"""
        return self.get_acheteur().region.nom if self.get_acheteur() else None

    def get_acheteur_pays(self):
        """Retourne le pays associé à l'acheteur"""
        return self.get_acheteur().pays.nom if self.get_acheteur() else None

    def get_acheteur_addresse(self):
        """Retourne l'adresse associée à l'acheteur"""
        return self.get_acheteur().adresse.nom if self.get_acheteur() else None