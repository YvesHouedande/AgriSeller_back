from django.contrib import admin
from .models import (
    CategorieCulture,
    Culture,
    ExploitationAgricole,
    ExploitationCulture
)

class ExploitationCultureInline(admin.TabularInline):
    model = ExploitationCulture
    extra = 0

@admin.register(CategorieCulture)
class CategorieCultureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation')
    search_fields = ('nom',)

@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'saison_plantation')
    list_filter = ('categorie', 'saison_plantation')
    filter_horizontal = ('regions',)

@admin.register(ExploitationAgricole)
class ExploitationAgricoleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'producteur', 'superficie', 'statut')
    list_filter = ('statut', 'type_propriete')
    inlines = [ExploitationCultureInline]
    raw_id_fields = ('producteur_physique', 'producteur_organisation')

@admin.register(ExploitationCulture)
class ExploitationCultureAdmin(admin.ModelAdmin):
    list_display = ('culture', 'exploitation', 'date_plantation')
    list_filter = ('methode',)