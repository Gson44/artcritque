from django.contrib import admin
from .models import ArtUser, ArtEntry
# Register your models here.


admin.site.register(ArtUser)
admin.site.register(ArtEntry)