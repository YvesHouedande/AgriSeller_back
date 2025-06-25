from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import Notification

class NotificationService:
    
    @classmethod
    def _send_ws_notification(cls, user, notification_data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifs_{user.id}",
            {
                "type": "send.notification",
                "notification": notification_data
            }
        )

    @classmethod
    def create_notification(cls, user, notif_type, title, message, metadata=None):
        """Crée et envoie une notification"""
        notification = Notification.objects.create(
            user=user,
            type=notif_type,
            title=title,
            message=message,
            metadata=metadata or {}
        )
        
        # Préparer les données pour WebSocket
        ws_data = {
            'id': str(notification.id),
            'type': notif_type,
            'title': title,
            'message': message,
            'timestamp': timezone.now().isoformat(),
            'metadata': metadata or {}
        }
        
        # Envoyer via WebSocket
        cls._send_ws_notification(user, ws_data)
        
        return notification

    # Cas spécifiques
    @classmethod
    def notifier_creation_offre(cls, offre):
        validateurs = User.objects.filter(role='VALID', zone=offre.ville.region)
        for validateur in validateurs:
            cls.create_notification(
                user=validateur,
                notif_type=Notification.NotificationType.OFFRE_CREEE,
                title="Nouvelle offre à valider",
                message=f"Offre #{offre.id} - {offre.culture.nom}",
                metadata={
                    'offre_id': str(offre.id),
                    'action_url': f"/offres/{offre.id}/valider"
                }
            )

    @classmethod
    def notifier_validation_offre(cls, offre, est_validee):
        notif_type = (Notification.NotificationType.OFFRE_VALIDEE if est_validee
                     else Notification.NotificationType.OFFRE_REJETEE)
        cls.create_notification(
            user=offre.producteur.user,
            notif_type=notif_type,
            title="Statut de votre offre",
            message=f"Votre offre #{offre.id} a été {'validée' if est_validee else 'rejetée'}",
            metadata={
                'offre_id': str(offre.id),
                'raison': getattr(offre, 'motif_rejet', None)
            }
        )

    # ... Ajouter toutes les autres méthodes pour vos scénarios