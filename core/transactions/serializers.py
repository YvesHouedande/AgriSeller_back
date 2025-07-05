from rest_framework import serializers
from .models import Offre, MouvementStock, Commande
from core.localisation.serializers import VilleSerializer
from core.productions.serializers import CultureSerializer

class OffreSerializer(serializers.ModelSerializer):
    culture = CultureSerializer()
    lieu_retrait = VilleSerializer()
    producteur_details = serializers.SerializerMethodField()
    quantite_actuelle = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Offre
        fields = '__all__'
        read_only_fields = ('id', 'date_publication', 'est_valide')

    def get_producteur_details(self, obj):
        return obj.get_producteur_details()

class MouvementStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouvementStock
        fields = '__all__'
        read_only_fields = ('id', 'date', 'utilisateur')

class CreateOffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        exclude = ('est_valide', 'producteur_physique', 'producteur_organisation')

    def create(self, validated_data):
        # user = self.context['request'].user
        # if hasattr(user, 'producteur_personnephysique'):
        #     validated_data['producteur_physique'] = user.producteur_personnephysique
        # elif hasattr(user, 'producteur_organisation'):
        #     validated_data['producteur_organisation'] = user.producteur_organisation
        
        offre = super().create(validated_data)
        
        # Envoi notification aux validateurs
        from core.notifications.services import notify_validators
        notify_validators(
            'OFFRE_CREEE',
            'Nouvelle offre à valider',
            f"Une nouvelle offre de {offre.nom_produit} a été créée",
            {
                'offre_id': str(offre.id),
                'producteur_type': offre.get_producteur_type()
            }
        )
        
        return offre


# serializers.py
class CommandeSerializer(serializers.ModelSerializer):
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    offre_details = serializers.SerializerMethodField()
    acheteur_details = serializers.SerializerMethodField()
    validateur_details = serializers.SerializerMethodField()

    class Meta:
        model = Commande
        fields = [
            'id',
            'offre',
            'offre_details',
            'acheteur_details',
            'validateur_details',
            'quantite',
            'statut',
            'statut_display',
            'date_creation',
            'date_maj'
        ]
        read_only_fields = ['statut', 'date_creation', 'date_maj']

    def get_offre_details(self, obj):
        from core.transactions.serializers import OffreSerializer
        return OffreSerializer(obj.offre).data

    def get_acheteur_details(self, obj):
        return obj.get_acheteur_details()

    def get_validateur_details(self, obj):
        if not obj.validateur:
            return None
        return {
            'id': obj.validateur.id,
            'telephone': obj.validateur.telephone,
        }



class UpdateStatutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = ['statut']