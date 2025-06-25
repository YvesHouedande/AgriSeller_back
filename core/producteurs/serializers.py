from rest_framework import serializers
from core.accounts.models import User
from .models import ProducteurPersonnePhysique, ProducteurOrganisation



class CompletudeProducteurSerializer(serializers.Serializer):
    complet = serializers.BooleanField()
    type_producteur = serializers.CharField(required=False)
    champs_manquants = serializers.ListField(child=serializers.CharField())
    pourcentage_completion = serializers.IntegerField()


class BaseProducteurSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    user = serializers.SerializerMethodField(read_only=True)
    
    def get_user(self, obj):
        from core.accounts.serializers import UserSerializer
        return UserSerializer(obj.user).data

    class Meta:
        abstract = True

class ProducteurPhysiqueSerializer(BaseProducteurSerializer):
    class Meta:
        model = ProducteurPersonnePhysique
        fields = [
            'id', 'user', 'experience_agricole', 'certification',
            'telephone', 'site_web', 'facebook', 'whatsapp', 'adresse',
            'ville', 'region', 'pays', 'actif', 'date_creation', 'date_maj',
            'date_naissance', 'lieu_naissance', 'numero_cni',
            'situation_matrimoniale', 'nombre_enfants',
            'contact_urgence_nom', 'contact_urgence_telephone'
        ]
        extra_kwargs = {
            'numero_cni': {'required': False},
            'date_naissance': {'required': False}
        }

class ProducteurPhysiqueDetailSerializer(ProducteurPhysiqueSerializer):
    class Meta(ProducteurPhysiqueSerializer.Meta):
        depth = 1

class ProducteurOrganisationSerializer(BaseProducteurSerializer):
    class Meta:
        model = ProducteurOrganisation
        fields = [
            'id', 'user', 'experience_agricole', 'certification',
            'telephone', 'site_web', 'facebook', 'whatsapp', 'adresse',
            'ville', 'region', 'pays', 'actif', 'date_creation', 'date_maj',
            'raison_sociale', 'type_organisation', 'numero_registre',
            'nom_dirigeant', 'fonction_dirigeant', 'nombre_membres',
            'capital_social'
        ]
        extra_kwargs = {
            'numero_registre': {'required': False},
            'capital_social': {'required': False}
        }

class ProducteurOrganisationDetailSerializer(ProducteurOrganisationSerializer):
    class Meta(ProducteurOrganisationSerializer.Meta):
        depth = 1