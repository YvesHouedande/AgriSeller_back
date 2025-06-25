# producteurs/admin.py
from django.contrib import admin
from .models import ProducteurPersonnePhysique, ProducteurOrganisation

@admin.register(ProducteurPersonnePhysique)
class ProducteurPhysiqueAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_age', 'certification', 'ville')
    list_filter = ('certification', 'ville__region')
    search_fields = ('user__first_name', 'user__last_name', 'numero_cni')

@admin.register(ProducteurOrganisation)
class ProducteurOrganisationAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'type_organisation', 'ville')
    list_filter = ('type_organisation', 'ville__region')
    search_fields = ('raison_sociale', 'numero_registre')