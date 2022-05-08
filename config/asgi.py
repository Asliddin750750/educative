import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import common.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket_demo.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            common.routing.websocket_urlpatterns
        )
    )
})
