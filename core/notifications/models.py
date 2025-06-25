from django.db import models
from django.contrib.auth import get_user_model

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        OFFRE_CREEE = 'OFFRE_CREEE', 'Nouvelle offre créée'
        OFFRE_VALIDEE = 'OFFRE_VALIDEE', 'Offre validée'
        OFFRE_REJETEE = 'OFFRE_REJETEE', 'Offre rejetée'
        COMMANDE_CREEE = 'COMMANDE_CREEE', 'Nouvelle commande'
        COMMANDE_EN_COURS = 'COMMANDE_EN_COURS', 'Commande en traitement'
        COMMANDE_TERMINEE = 'COMMANDE_TERMINEE', 'Commande terminée'
        NOUVELLE_PROPOSITION = 'NOUVELLE_PROPOSITION', 'Nouvelle proposition'
        PROPOSITION_CONFIRMEE = 'PROPOSITION_CONFIRMEE', 'Proposition confirmée'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=NotificationType.choices)
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]

    def mark_as_read(self):
        self.is_read = True
        self.save()