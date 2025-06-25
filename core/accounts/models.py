from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from django.core.validators import RegexValidator


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
        COMMERCANT = 'COMM', 'Commerçant'
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