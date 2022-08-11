# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
 
# import websocketUnsubscribe.routing
 
# django_asgi_app = get_asgi_application()
# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             websocketUnsubscribe.routing.websocket_urlpatterns
#         )
#     ),
# })

from django.urls import path, re_path
from websocketUnsubscribe.consumers import AsyncConsumer

websocket_urlpatterns = [
    re_path(r'mes/', AsyncConsumer.as_asgi()),
]