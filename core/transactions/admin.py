from django.contrib import admin
from core.transactions.models import Offre, MouvementStock, Commande, PropositionProducteur

class MouvementStockInline(admin.TabularInline):
    model = MouvementStock
    extra = 0
    fields = ('id', 'type_mouvement', 'quantite', 'date', 'utilisateur', 'notes')
    readonly_fields = ('id', 'date')
    show_change_link = True

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_produit', 'producteur', 'quantite_actuelle', 'prix_unitaire', 'est_active')
    list_display_links = ('id', 'nom_produit')
    list_filter = ('est_active', 'culture', 'lieu_retrait')
    search_fields = ('nom_produit', 'description', 'id')
    readonly_fields = ('id', 'date_publication')
    inlines = [MouvementStockInline]
    fieldsets = (
        ('Informations de base', {
            'fields': ('id', 'nom_produit', 'producteur_physique', 'producteur_organisation', 'description')
        }),
        ('Détails', {
            'fields': ('culture', 'quantite_initiale', 'seuil_alerte', 'unite', 'prix_unitaire')
        }),
        ('Statut', {
            'fields': ('est_valide', 'est_active')
        }),
        ('Localisation', {
            'fields': ('lieu_retrait',)
        }),
        ('Dates', {
            'fields': ('date_publication', 'date_expiration')
        }),
    )

    def producteur(self, obj):
        return obj.producteur_physique or obj.producteur_organisation
    producteur.short_description = 'Producteur'

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_id', 'client', 'offre', 'quantite', 'statut', 'date_creation')
    list_display_links = ('id', 'short_id')
    list_filter = ('statut', 'offre__culture')
    search_fields = ('id', 'client__username', 'offre__nom_produit')
    readonly_fields = ('id', 'date_creation', 'date_maj')
    date_hierarchy = 'date_creation'
    
    def short_id(self, obj):
        return f"CMD-{obj.id}"
    short_id.short_description = "Réf."

@admin.register(PropositionProducteur)
class PropositionProducteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'commande', 'offre', 'quantite_demandee', 'statut', 'date_validation')
    list_filter = ('statut',)
    search_fields = ('id', 'commande__id', 'offre__nom_produit')
    readonly_fields = ('id',)
    raw_id_fields = ('commande', 'offre')