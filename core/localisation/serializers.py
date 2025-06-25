# localisation/serializers.py
from rest_framework import serializers
from core.localisation.models import Pays, Region, Ville

class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'
        read_only_fields = ('id',)

class RegionSerializer(serializers.ModelSerializer):
    pays = PaysSerializer(read_only=True)
    
    class Meta:
        model = Region
        fields = '__all__'
        read_only_fields = ('id',)

class VilleSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    
    class Meta:
        model = Ville
        fields = ['id', 'nom', 'region', 'code_postal']
        read_only_fields = ('id',)

class VilleDetailSerializer(VilleSerializer):
    region = RegionSerializer()
    pays = serializers.SerializerMethodField()
    
    def get_pays(self, obj):
        return PaysSerializer(obj.region.pays).data
    
    class Meta(VilleSerializer.Meta):
        fields = VilleSerializer.Meta.fields + ['pays']

