import os
import django
from django.core.asgi import get_asgi_application

# Configuration initiale Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgriSeller_back.settings')
django.setup()  # Important pour résoudre les problèmes d'import

# Importez les dépendances Channels APRÈS django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from core.notifications.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})