from django.contrib import admin

from .models import Album
from .models import Autor
from .models import Cancion


admin.site.register(Autor)
admin.site.register(Album)
admin.site.register(Cancion)
