from django.contrib import admin
from .models import *

# Register your models here.
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ["name","user","custom_name","obj_type"]
    search_fields = ["user__username"]

# Registered Favourites Model for viewing favourites
admin.site.register(Favourites,FavouritesAdmin)