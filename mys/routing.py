from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from mys.consumers import ChatConsumer

#application = ProtocolTypeRouter({
#    'websocket': URLRouter([
#        path('MYSApp/progressInfo/', ChatConsumer.as_asgi()),
#    ])
#})

from . import consumers

websocket_urlpatterns = [
    path('MYSApp/progressInfo/', consumers.ChatConsumer.as_asgi()),
]

print("Routing was called")