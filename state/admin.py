from django.contrib import admin
from .models import PAU 

class PAUAdmin(admin.ModelAdmin):
    model=PAU
    ordering=["-objectid_1"]

admin.site.register(PAU)

# Register your models here.
