# transactions/admin.py
from django.contrib import admin
from core.transactions.models import Offre, MouvementStock, Commande, PropositionProducteur

class MouvementStockInline(admin.TabularInline):
    model = MouvementStock
    extra = 0

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('nom_produit', 'producteur', 'quantite_actuelle', 'prix_unitaire', 'est_active')
    list_filter = ('est_active', 'culture', 'lieu_retrait')
    search_fields = ('nom_produit', 'description')
    inlines = [MouvementStockInline]

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'offre', 'quantite', 'statut', 'date_commande')
    list_filter = ('statut', 'offre__culture')
    search_fields = ('client__username', 'offre__nom_produit')

@admin.register(PropositionProducteur)
class PropositionProducteurAdmin(admin.ModelAdmin):
    list_display = ('commande', 'offre', 'quantite_demandee', 'statut')
    list_filter = ('statut',)