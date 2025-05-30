"""
ASGI config for chairs_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chairs_project import urls_ws

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chairs_project.settings")

application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": URLRouter(urls_ws.urlpatterns),
    },
)
