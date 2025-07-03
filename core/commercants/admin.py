# core/commercants/admin.py
from django.contrib import admin
from .models import AcheteurPersonnePhysique, AcheteurOrganisation

@admin.register(AcheteurPersonnePhysique)
class AcheteurPersonnePhysiqueAdmin(admin.ModelAdmin):
    list_display = ('user', 'type_commerce', 'ville', 'actif')
    list_filter = ('type_commerce', 'ville', 'actif')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('user', 'date_naissance', 'lieu_naissance', 'numero_cni')
        }),
        ('Informations professionnelles', {
            'fields': ('type_commerce', 'experience_commerciale')
        }),
        ('Localisation', {
            'fields': ('adresse', 'ville', 'region', 'pays')
        }),
        ('Statut', {
            'fields': ('actif',)
        }),
    )

@admin.register(AcheteurOrganisation)
class AcheteurOrganisationAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'forme_juridique', 'type_commerce', 'ville', 'actif')
    list_filter = ('forme_juridique', 'type_commerce', 'ville', 'actif')
    search_fields = ('raison_sociale', 'numero_registre', 'nom_dirigeant')
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user',)
        }),
        ('Informations légales', {
            'fields': ('raison_sociale', 'forme_juridique', 'numero_registre', 'date_immatriculation', 'type_commerce')
        }),
        ('Dirigeant', {
            'fields': ('nom_dirigeant', 'fonction_dirigeant')
        }),
        ('Informations financières', {
            'fields': ('nombre_employes', 'chiffre_affaires_annuel', 'iban', 'nom_banque')
        }),
        ('Localisation', {
            'fields': ('adresse', 'ville', 'region', 'pays')
        }),
        ('Statut', {
            'fields': ('actif',)
        }),
    )