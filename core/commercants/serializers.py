# core/commercants/serializers.py
from rest_framework import serializers
from .models import AcheteurPersonnePhysique, AcheteurOrganisation
from core.localisation.serializers import VilleSerializer, RegionSerializer, PaysSerializer

class BaseAcheteurSerializer(serializers.ModelSerializer):
    ville = VilleSerializer(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    
    def get_user(self, obj):
        from core.accounts.serializers import UserSerializer
        return UserSerializer(obj.user).data
    
    class Meta:
        fields = [
            'id', 'user', 'experience_commerciale', 
            'site_web', 'facebook', 'whatsapp', 'instagram',
            'adresse', 'ville', 'horaires_ouverture', 'actif',
            'date_creation', 'date_maj'
        ]

class AcheteurPersonnePhysiqueSerializer(BaseAcheteurSerializer):
    class Meta(BaseAcheteurSerializer.Meta):
        model = AcheteurPersonnePhysique
        fields = BaseAcheteurSerializer.Meta.fields + [
            'date_naissance', 'lieu_naissance', 'numero_cni',
            'situation_matrimoniale', 'contact_urgence_nom', 'contact_urgence_telephone'
        ]

class AcheteurOrganisationSerializer(BaseAcheteurSerializer):
    class Meta(BaseAcheteurSerializer.Meta):
        model = AcheteurOrganisation
        fields = BaseAcheteurSerializer.Meta.fields + [
            'raison_sociale', 'forme_juridique', 'numero_registre',
            'date_immatriculation', 'nom_dirigeant', 'fonction_dirigeant',
            'nombre_employes', 'chiffre_affaires_annuel', 'iban', 'nom_banque'
        ]




# A Voir plus tard si on veut l'utiliser
class CompletudeAcheteurSerializer(serializers.Serializer):
    complet = serializers.BooleanField()
    champs_manquants = serializers.ListField(child=serializers.CharField())
    pourcentage_completion = serializers.IntegerField()