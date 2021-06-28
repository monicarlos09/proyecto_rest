from django.urls import path
from canciones.views import CancionViewSet

app_name = 'canciones'

canciones_list = CancionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

canciones_detail = CancionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})


urlpatterns = [
    path('', canciones_list),
    path('<int:pk>', canciones_detail),
]
