# productions/admin.py
from django.contrib import admin
from core.productions.models import (
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
    list_display = ('nom',)
    search_fields = ('nom', 'description')

@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'saison_plantation', 'duree_cycle', 'active')
    list_filter = ('categorie', 'saison_plantation', 'active')
    search_fields = ('nom', 'nom_scientifique')
    filter_horizontal = ('regions',)

@admin.register(ExploitationAgricole)
class ExploitationAgricoleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'producteur', 'superficie', 'type_propriete', 'statut')
    list_filter = ('statut', 'type_propriete')
    search_fields = ('nom', 'adresse')
    inlines = [ExploitationCultureInline]

    def producteur(self, obj):
        return obj.producteur_physique or obj.producteur_organisation

@admin.register(ExploitationCulture)
class ExploitationCultureAdmin(admin.ModelAdmin):
    list_display = ('exploitation', 'culture', 'methode', 'superficie_allouee')
    list_filter = ('methode', 'culture')
    search_fields = ('exploitation__nom', 'culture__nom')