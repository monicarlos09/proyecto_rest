from artista.views import ArtistaViewSet
from django.urls import path

app_name = "artista"

artista_list = ArtistaViewSet.as_view({"get": "list", "post": "create"})

artista_detail = ArtistaViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


urlpatterns = [
    path("", artista_list),
    path("<int:pk>", artista_detail),
]
