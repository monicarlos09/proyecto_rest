from django.urls import path
from disquera.views import DisqueraViewSet

app_name = 'disquera'

disquera_list = DisqueraViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

disquera_detail = DisqueraViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})


urlpatterns = [
    path('', disquera_list),
    path('<int:pk>', disquera_detail),
]
