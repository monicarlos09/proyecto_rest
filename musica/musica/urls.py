from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('canciones/', include('canciones.urls')),
    path('artista/', include('artista.urls')),
    path('disquera/', include('disquera.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
