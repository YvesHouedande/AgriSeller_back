from django.db import models
import uuid
from core.accounts.models import User

class Commercant(models.Model):
    TYPES_COMMERCANTS = [
        ('detaillant', 'Détaillant'),
        ('grossiste', 'Grossiste'),
        ('transformateur', 'Transformateur'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_commercant = models.CharField(max_length=20, choices=TYPES_COMMERCANTS)
    
    # Informations professionnelles
    annee_experience = models.PositiveIntegerField(default=0)
    zone_achat_preferee = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "Commerçant"
        verbose_name_plural = "Commerçants"
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_type_commercant_display()})"