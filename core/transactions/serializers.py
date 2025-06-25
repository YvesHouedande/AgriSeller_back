# transactions/serializers.py
from rest_framework import serializers
from core.transactions.models import Offre, MouvementStock, Commande, PropositionProducteur
from core.accounts.serializers import UserSerializer
from core.producteurs.serializers import ProducteurPhysiqueSerializer, ProducteurOrganisationSerializer
# from core.cultures.serializers import CultureSerializer
# from core.localisation.serializers import VilleSerializer

class OffreSerializer(serializers.ModelSerializer):
    culture = CultureSerializer()
    lieu_retrait = VilleSerializer()
    producteur_details = serializers.SerializerMethodField()
    quantite_actuelle = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Offre
        fields = '__all__'
        read_only_fields = ('id', 'date_publication', 'quantite_actuelle')

    def get_producteur_details(self, obj):
        return obj.get_producteur_details()

class MouvementStockSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)

    class Meta:
        model = MouvementStock
        fields = '__all__'
        read_only_fields = ('id', 'date')

class CommandeSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    offre = OffreSerializer(read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)

    class Meta:
        model = Commande
        fields = '__all__'
        read_only_fields = ('id', 'date_commande')

class PropositionProducteurSerializer(serializers.ModelSerializer):
    commande = CommandeSerializer(read_only=True)
    offre = OffreSerializer(read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)

    class Meta:
        model = PropositionProducteur
        fields = '__all__'