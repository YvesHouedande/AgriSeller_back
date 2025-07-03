from rest_framework import serializers
from .models import (
    CategorieCulture,
    Culture,
    ExploitationAgricole,
    ExploitationCulture
)
from core.localisation.serializers import RegionSerializer

class CategorieCultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieCulture
        fields = '__all__'

class CultureSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)
    categorie = CategorieCultureSerializer()

    class Meta:
        model = Culture
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_maj')

class ExploitationAgricoleSerializer(serializers.ModelSerializer):
    producteur_details = serializers.SerializerMethodField()

    class Meta:
        model = ExploitationAgricole
        exclude = ('producteur_physique', 'producteur_organisation')
        read_only_fields = ('id', 'date_creation', 'date_maj')

    def get_producteur_details(self, obj):
        producteur = obj.producteur
        if hasattr(producteur, 'user'):
            return {
                'type': 'physique',
                'nom': producteur.user.get_full_name(),
                'telephone': producteur.user.telephone
            }
        else:
            return {
                'type': 'organisation',
                'raison_sociale': producteur.raison_sociale,
                'telephone': producteur.user.telephone
            }

class ExploitationCultureSerializer(serializers.ModelSerializer):
    culture = CultureSerializer()
    exploitation = serializers.StringRelatedField()

    class Meta:
        model = ExploitationCulture
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_maj')