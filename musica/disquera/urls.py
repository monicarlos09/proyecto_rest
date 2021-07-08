from disquera.views import DisqueraViewSet
from django.urls import path

app_name = "disquera"

disquera_list = DisqueraViewSet.as_view({"get": "list", "post": "create"})

disquera_detail = DisqueraViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


urlpatterns = [
    path("", disquera_list, name="lista"),
    path("<int:pk>", disquera_detail, name="detalle"),
]
