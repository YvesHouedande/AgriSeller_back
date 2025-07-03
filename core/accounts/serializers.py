from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import RegexValidator
from core.accounts.models import User
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'telephone', 'first_name', 'last_name', 'email', 'role', 'is_active']
        read_only_fields = ['id', 'is_active']

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

    def validate(self, attrs):
        attrs[self.username_field] = attrs.get('telephone')
        return super().validate(attrs)

class UserRegisterSerializer(serializers.ModelSerializer):
    telephone = serializers.CharField(
        validators=[RegexValidator(regex=r'^\+?[0-9]{9,15}$')],
        required=True
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    role = serializers.ChoiceField(
        choices=User.Role.choices,
        required=True
    )
    
    class Meta:
        model = User
        fields = ['telephone', 'password', 'role']
        
    def validate_telephone(self, value):
        if self.context.get('is_create') and User.objects.filter(telephone=value).exists():
            raise serializers.ValidationError("Ce numéro est déjà utilisé")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            telephone=validated_data['telephone'],
            password=validated_data['password'],
            role=validated_data['role'],
            first_name='',
            last_name=''
        )


class CompletudeProducteurSerializer(serializers.Serializer):
    complet = serializers.BooleanField()
    type_producteur = serializers.CharField(required=False)
    champs_manquants = serializers.ListField(child=serializers.CharField())
    pourcentage_completion = serializers.IntegerField()


class UserProducteurListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()
    producteur = serializers.SerializerMethodField()
    producteur_type = serializers.SerializerMethodField()
    ville = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    pays = serializers.SerializerMethodField()
    adresse = serializers.SerializerMethodField()
    certification = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 
            'telephone', 
            'email', 
            'full_name',
            'role', 
            'role_display',
            'is_verified', 
            'is_active',
            'date_inscription',
            'photo_profil',
            'producteur',  
            'producteur_type',
            'ville',
            'region',
            'pays',
            'adresse',
            'certification'
        ]

    def get_certification(self, obj):
        producteur = obj.get_producteur()
        if producteur:
            return producteur.certification
        return None
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def get_role_display(self, obj):
        return obj.get_role_display()

    def get_producteur(self, obj):
        producteur = obj.get_producteur()
        if producteur:
            # Vous pouvez retourner un dictionnaire avec les infos clés ou l'ID
            return {
                'id': producteur.id,
                'nom': getattr(producteur, 'nom', None) or getattr(producteur, 'raison_sociale', None),
                'adresse': getattr(producteur, 'adresse', None)
            }
        return None

    def get_producteur_type(self, obj):
        return obj.get_producteur_type()

    def get_ville(self, obj):
        return obj.get_producteur_ville()

    def get_region(self, obj):
        return obj.get_producteur_region()

    def get_pays(self, obj):
        return obj.get_producteur_pays()

    def get_adresse(self, obj):
        producteur = obj.get_producteur()
        return producteur.adresse if producteur else None


class UserAcheteurListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()
    acheteur = serializers.SerializerMethodField()
    acheteur_type = serializers.SerializerMethodField()
    ville = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    pays = serializers.SerializerMethodField()
    adresse = serializers.SerializerMethodField()
    type_commerce = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 
            'telephone', 
            'email', 
            'full_name',
            'role', 
            'role_display',
            'is_verified', 
            'is_active',
            'date_inscription',
            'photo_profil',
            'acheteur',  
            'acheteur_type',
            'type_commerce',
            'ville',
            'region',
            'pays',
            'adresse',
        ]

    def get_acheteur(self, obj):
        acheteur = obj.get_acheteur()
        if acheteur:
            # Vous pouvez retourner un dictionnaire avec les infos clés ou l'ID
            return {
                'id': acheteur.id,
                'nom': getattr(acheteur, 'nom', None) or getattr(acheteur, 'raison_sociale', None),
                'adresse': getattr(acheteur, 'adresse', None),
                'fonction_dirigeant': getattr(acheteur, 'fonction_dirigeant', None),
                'type_organisation': getattr(acheteur, 'type_organisation', None),
                'forme_juridique': getattr(acheteur, 'forme_juridique', None)
            }
        return None
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def get_role_display(self, obj):
        return obj.get_role_display()

    # def get_producteur(self, obj):
    #     producteur = obj.get_producteur()
    #     if producteur:
    #         # Vous pouvez retourner un dictionnaire avec les infos clés ou l'ID
    #         return {
    #             'id': producteur.id,
    #             'nom': getattr(producteur, 'nom', None) or getattr(producteur, 'raison_sociale', None),
    #             'adresse': getattr(producteur, 'adresse', None)
    #         }
    #     return None

    # def get_producteur_type(self, obj):
    #     return obj.get_producteur_type()

    def get_ville(self, obj):
        acheteur = obj.get_acheteur()
        if acheteur:
            return acheteur.ville.nom if acheteur.ville else None
        return None

    def get_region(self, obj):
        acheteur = obj.get_acheteur()
        if acheteur:
            return acheteur.region.nom if acheteur.region else None
        return None

    def get_pays(self, obj):
        acheteur = obj.get_acheteur()
        if acheteur:
            return acheteur.pays.nom if acheteur.pays else None
        return None

    def get_adresse(self, obj):
        acheteur = obj.get_acheteur()
        if acheteur:
            return acheteur.adresse if acheteur.adresse else None
        return None

    def get_acheteur_type(self, obj):
        return obj.get_acheteur_type()

    def get_type_commerce(self, obj):
        acheteur = obj.get_acheteur()
        if acheteur:
            return acheteur.type_commerce if acheteur.type_commerce else None
        return None 