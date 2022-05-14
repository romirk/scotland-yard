from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from . import views
from .patterns import UUID_RE

urlpatterns = [
    path("", views.index, name="index"),
    path("error/<str:error>", views.index, name="indexerror"),
    path("lobby", views.lobby, name="lobby"),
    path("game", views.game, name="game"),
    path("info", views.info, name="info"),
    path("map", views.map, name="map"),
    re_path(r"^(?P<game_id>" + UUID_RE + ")$", views.index),
] + static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
