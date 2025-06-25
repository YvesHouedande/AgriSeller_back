# localisation/admin.py
from django.contrib import admin
from core.localisation.models import Pays, Region, Ville

class VilleInline(admin.TabularInline):
    model = Ville
    extra = 0

class RegionInline(admin.TabularInline):
    model = Region
    extra = 0

@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code_iso')
    search_fields = ('nom', 'code_iso')
    inlines = [RegionInline]

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'pays')
    list_filter = ('pays',)
    search_fields = ('nom', 'code')
    inlines = [VilleInline]

@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'region', 'code_postal')
    list_filter = ('region', 'region__pays')
    search_fields = ('nom', 'code_postal')