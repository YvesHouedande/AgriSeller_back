# productions/serializers.py
from rest_framework import serializers
from core.productions.models import (
    CategorieCulture,
    Culture,
    ExploitationAgricole,
    ExploitationCulture
)
from core.localisation.serializers import RegionSerializer
from core.producteurs.serializers import (
    ProducteurPhysiqueSerializer,
    ProducteurOrganisationSerializer
)

class CategorieCultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieCulture
        fields = '__all__'

class CultureSerializer(serializers.ModelSerializer):
    categorie = CategorieCultureSerializer()
    regions = RegionSerializer(many=True)
    
    class Meta:
        model = Culture
        fields = '__all__'
        read_only_fields = ('id',)

class ExploitationAgricoleSerializer(serializers.ModelSerializer):
    producteur_details = serializers.SerializerMethodField()
    
    class Meta:
        model = ExploitationAgricole
        fields = '__all__'
        read_only_fields = ('id', 'date_creation')
    
    def get_producteur_details(self, obj):
        if obj.producteur_physique:
            return ProducteurPhysiqueSerializer(obj.producteur_physique).data
        elif obj.producteur_organisation:
            return ProducteurOrganisationSerializer(obj.producteur_organisation).data
        return None

class ExploitationCultureSerializer(serializers.ModelSerializer):
    culture = CultureSerializer()
    exploitation = ExploitationAgricoleSerializer()
    
    class Meta:
        model = ExploitationCulture
        fields = '__all__'
        read_only_fields = ('id',)