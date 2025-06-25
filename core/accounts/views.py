from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .docs.auth_docs import LOGIN_DOCS, REGISTER_DOCS
from .serializers import CustomTokenSerializer, UserRegisterSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

# @extend_schema_view(post=LOGIN_DOCS)
class LoginView(TokenObtainPairView):
    """
    Endpoint de connexion principal. 
    Utilise le numéro de téléphone comme identifiant.
    """
    serializer_class = CustomTokenSerializer

# @extend_schema_view(post=REGISTER_DOCS)
class RegisterView(generics.CreateAPIView):
    """
    Endpoint d'enregistrement.
    Retourne uniquement les tokens JWT après création réussie.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED)
            
        except DRFValidationError as e:
            return Response({
                "error": "Erreur de validation",
                "details": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except DjangoValidationError as e:
            return Response({
                "error": "Erreur de validation",
                "details": e.message_dict
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "error": "Erreur lors de la création du compte",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)