from django.db import models
import uuid
from core.accounts.models import User
from core.localisation.models import Ville
from core.producteurs.models import ProducteurPersonnePhysique, ProducteurOrganisation
from core.cultures.models import Culture
from core.transactions.models import Commande
from core.validation.models import Validation



class Offre(models.Model):
    UNITES = [
        ('kg', 'Kilogramme'),
        ('g', 'Gramme'), 
        ('l', 'Litre'),
        ('unite', 'Unité'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relations polymorphiques avec les producteurs
    producteur_physique = models.ForeignKey(
        ProducteurPersonnePhysique,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='offres_physique'
    )
    producteur_organisation = models.ForeignKey(
        ProducteurOrganisation,
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
        related_name='offres_organisation'
    )
    
    # Détails du produit
    culture = models.ForeignKey(Culture, on_delete=models.PROTECT)
    quantite_initiale = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seuil_alerte = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unite = models.CharField(max_length=10, choices=UNITES)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    est_valide = models.BooleanField(default=True, help_text="Indique si l'offre est validée par le centre de validation")
    est_active = models.BooleanField(default=True, help_text="Indique si l'offre est active et visible pour les clients")
    nom_produit = models.CharField(max_length=200, help_text="Nom du produit ou de l'offre")
    description = models.TextField(blank=True, help_text="Description détaillée de l'offre")
    
    
    # Localisation
    lieu_retrait = models.ForeignKey(Ville, on_delete=models.CASCADE)
    
    # Image
    photo_produit = models.ImageField(upload_to='offres/', blank=True)
    
    # Dates
    date_publication = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField()
    
    class Meta:
        verbose_name = "Offre"
        verbose_name_plural = "Offres"
        ordering = ['-date_publication']

    @property
    def quantite_actuelle(self):
        """Calcule dynamiquement le stock restant"""
        return self.quantite_initiale - sum(
            mouvement.quantite 
            for mouvement in self.mouvements.filter(
                type_mouvement__in=['COMMANDE', 'SUPPRESSION']
            )
        )
    
    @property
    def producteur(self):
        """Retourne le producteur quel que soit son type"""
        return self.producteur_physique or self.producteur_organisation
    
    def save(self, *args, **kwargs):
        """Validation : un seul type de producteur doit être défini"""
        if not (self.producteur_physique or self.producteur_organisation):
            raise ValueError("Un producteur (physique ou organisation) doit être spécifié")
        if self.producteur_physique and self.producteur_organisation:
            raise ValueError("Uniquement un type de producteur peut être spécifié")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom_produit} par {self.producteur}"

    def get_producteur_type(self):
        """Retourne le type du producteur"""
        if self.producteur_physique:
            return 'physique'
        elif self.producteur_organisation:
            return 'organisation'
        return None

    def get_producteur_details(self):
        """Retourne les détails spécifiques au type de producteur"""
        if self.producteur_physique:
            return {
                'type': 'physique',
                'nom_complet': f"{self.producteur_physique.user.first_name} {self.producteur_physique.user.last_name}",
                'contact': self.producteur_physique.user.telephone
            }
        elif self.producteur_organisation:
            return {
                'type': 'organisation',
                'raison_sociale': self.producteur_organisation.raison_sociale,
                'contact': self.producteur_organisation.user.telephone
            }
        return None


class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('COMMANDE', 'Vente client'),
        ('AJUSTEMENT', 'Correction manuelle'),
        ('SUPPRESSION', 'Retrait hors vente')
    ]

    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='mouvements')
    type_mouvement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantite = models.DecimalField(max_digits=10, decimal_places=2)  # Positif/négatif selon le type
    date = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date']



class Commande(models.Model):
    STATUT_CHOICES = [
        ('CONFIRMEE', 'Confirmée'),
        ('EN_COURS', 'En cours'),
        ('EN_ATENTE', 'En attente'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='commandes')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_commande = models.DateTimeField(auto_now_add=True)
    date_livraison = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date_commande']
    
    def __str__(self):
        return f"Commande #{self.id} - {self.offre.nom_produit} pour {self.client.username}"

        def quantite_restante(self):
        return self.quantite_demandee - sum(
            p.quantite_confirmee 
            for p in self.propositions.filter(statut='VALIDE_CENTRE')
        )

    def trouver_offres_complementaires(self):
        from django.db.models import Q
        
        return Offre.objects.filter(
            Q(culture=self.produit) &
            Q(quantite_actuelle__gt=0) &
            ~Q(id__in=self.propositions.values('offre_id'))
        ).order_by('prix_unitaire')


class PropositionProducteur(models.Model):
    STATUT_CHOICES = [
        ('PROPOSEE', 'Proposée par le centre'),
        ('CONFIRMEE_PRODUCTEUR', 'Confirmée par producteur'),
        ('VALIDE_CENTRE', 'Validée par le centre'),
        ('REFUSEE_PRODUCTEUR', 'Refusée par le producteur'),
        ('ANNULEE', 'Annulée')
    ]
    
    commande = models.ForeignKey('Commande', on_delete=models.CASCADE, related_name='propositions')
    offre = models.ForeignKey('Offre', on_delete=models.PROTECT)  # Lien direct à l'offre
    quantite_demandee = models.DecimalField(max_digits=12, decimal_places=2)  # Quantité initialement demandée
    quantite_confirmee = models.DecimalField(max_digits=12, decimal_places=2, null=True)  # Quantité réellement disponible
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='PROPOSEE')
    date_validation = models.DateTimeField(null=True)

    def clean(self):
        if self.quantite_confirmee and self.quantite_confirmee > self.offre.quantite_actuelle:
            raise ValidationError("Quantité confirmée > stock disponible")


    
