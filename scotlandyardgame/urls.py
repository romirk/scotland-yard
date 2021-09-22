from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lobby', views.lobby, name='lobby'),
    # path('new', views.new, name='new'),
    re_path(r'^(?P<game_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', views.index)
] + static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
