from django.urls import path

from . import views

app_name = 'disquera'
urlpatterns = [
    path('', views.DisqueraViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='canciones'),
]
