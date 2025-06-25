from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response({
        'count': notifications.count(),
        'results': serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(
        id=notification_id,
        user=request.user
    )
    notification.mark_as_read()
    return Response({'status': 'marked as read'})