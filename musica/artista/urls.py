from django.urls import path

from . import views

app_name = 'artista'
urlpatterns = [
    path('', views.ArtistaViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='artista'),
]
