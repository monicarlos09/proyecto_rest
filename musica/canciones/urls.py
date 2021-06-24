from django.urls import path

from . import views

app_name = 'canciones'
urlpatterns = [
    path('', views.CancionViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='canciones'),
]
