from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

# Fonction pour envoyer une notification à un utilisateur via WebSocket
def send_notification_to_user(user_id, notification_data):
    """ Focntion de base utilisee par les autres fonctions pour envoyer une notification via WebSocket """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_notification",
            "content": notification_data
        }
    )
    print(f"Notification sent to user {user_id}: {notification_data}")

# Fonction pour créer et envoyer une notification à un utilisateur
def create_and_send_notification(user, notification_type, title, message, metadata={}):
    """Utilise la fonction de base pour envoyer une notification à un utilisateur 
        aprés avoir creéé la notification dans la base de données.
    """
    notification = Notification.objects.create(
        user=user,
        type=notification_type,
        title=title,
        message=message,
        metadata=metadata
    )
    
    send_notification_to_user(
        user.id,
        {
            "id": str(notification.id),
            "type": notification.type,
            "title": notification.title,
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat(),
            "metadata": notification.metadata
        }
    )
    return notification

def notify_validators(notification_type, title, message, metadata={}):
    # Convertir tous les UUID en strings dans le metadata
    serializable_metadata = {
        k: str(v) if hasattr(v, 'hex') else v 
        for k, v in metadata.items()
    }
    validators = User.objects.filter(role='VALID', is_active=True)[:10]  # Limite à 10 validateurs actifs
    for validator in validators:
        create_and_send_notification(
            validator,
            notification_type,
            title,
            message,
            serializable_metadata
        )

