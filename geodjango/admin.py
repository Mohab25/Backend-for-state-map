from django.contrib import admin
from .models import *
from leaflet.admin import LeafletGeoAdmin

class SimpleLocationAdmin(LeafletGeoAdmin):
    pass

admin.site.register(SimpleLocation,SimpleLocationAdmin)
admin.site.register(roads,SimpleLocationAdmin)