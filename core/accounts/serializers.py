# from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.core.validators import RegexValidator
# from core.accounts.models import User
# from django.core.exceptions import ValidationError

# class CustomTokenSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['role'] = user.role

#         return token

#     def validate(self, attrs):
#         # Remplace 'username' par 'telephone' dans la validation
#         attrs[self.username_field] = attrs.get('telephone')
#         return super().validate(attrs)


# class UserRegisterSerializer(serializers.ModelSerializer):
#     telephone = serializers.CharField(
#         validators=[RegexValidator(regex=r'^\+?[0-9]{9,15}$')],
#         required=True
#     )
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         style={'input_type': 'password'}
#     )
#     role = serializers.ChoiceField(
#         choices=User.Role.choices,
#         required=True
#     )
    
#     class Meta:
#         model = User
#         fields = ['telephone', 'password', 'role']
        
#     def validate_telephone(self, value):
#         """Validation basée sur le regex uniquement en création"""
#         if self.context.get('is_create') and User.objects.filter(telephone=value).exists():
#             raise serializers.ValidationError("Ce numéro est déjà utilisé")
#         return value

#     def create(self, validated_data):
#         return User.objects.create_user(
#             telephone=validated_data['telephone'],
#             password=validated_data['password'],
#             role=validated_data['role'],
#             first_name='',  # Valeurs par défaut
#             last_name=''
#         )


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