from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import Offre, Commande, PropositionProducteur
from .services import NotificationService

@receiver(post_save, sender=Offre)
def handle_offre_notifications(sender, instance, created, **kwargs):
    if created:
        NotificationService.notifier_creation_offre(instance)
    elif instance.statut in ['VALIDE', 'REJETEE']:
        NotificationService.notifier_validation_offre(
            instance, 
            instance.statut == 'VALIDE'
        )

@receiver(post_save, sender=Commande)
def handle_commande_notifications(sender, instance, created, **kwargs):
    if created:
        NotificationService.notifier_nouvelle_commande(instance)
    elif instance.tracker.has_changed('statut'):
        NotificationService.notifier_statut_commande(
            instance,
            instance.tracker.previous('statut')
        )

@receiver(post_save, sender=PropositionProducteur)
def handle_proposition_notifications(sender, instance, created, **kwargs):
    if created:
        NotificationService.notifier_proposition_producteur(instance)