# transactions/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.transactions.models import Commande, MouvementStock

@receiver(post_save, sender=Commande)
def creer_mouvement_stock(sender, instance, created, **kwargs):
    if created and instance.statut == 'CONFIRMEE':
        MouvementStock.objects.create(
            offre=instance.offre,
            type_mouvement='COMMANDE',
            quantite=-instance.quantite,  # Négatif car sortie de stock
            utilisateur=instance.client
        )