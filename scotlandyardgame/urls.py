from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error/<str:error>", views.index, name="indexerror"),
    path("lobby", views.lobby, name="lobby"),
    path("game", views.game, name="game"),
    # path('map', views.map, name='map'),
    path("dot", views.dot, name="dot"),
    re_path(
        r"^(?P<game_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$",
        views.index,
    ),
] + static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
