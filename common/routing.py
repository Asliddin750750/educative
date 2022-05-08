from django.urls import re_path

from common import consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/$', consumers.NotificationConsumer.as_asgi())
]
