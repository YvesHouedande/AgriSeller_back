# core/commercants/serializers.py
from rest_framework import serializers
from .models import AcheteurPersonnePhysique, AcheteurOrganisation
from core.localisation.serializers import VilleSerializer, RegionSerializer, PaysSerializer

class BaseAcheteurSerializer(serializers.ModelSerializer):
    ville = VilleSerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    pays = PaysSerializer(read_only=True)
    
    ville_id = serializers.UUIDField(write_only=True)
    region_id = serializers.UUIDField(write_only=True)
    pays_id = serializers.UUIDField(write_only=True)

    class Meta:
        fields = [
            'id', 'user', 'experience_commerciale', 'type_acheteur',
            'site_web', 'facebook', 'whatsapp', 'instagram',
            'adresse', 'ville', 'region', 'pays', 'ville_id', 'region_id', 'pays_id',
            'horaires_ouverture', 'actif', 'date_creation', 'date_maj'
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