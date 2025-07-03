from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenSerializer, UserRegisterSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.permissions import IsAuthenticated
from .serializers import CompletudeProducteurSerializer
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from .serializers import UserProducteurListSerializer, UserAcheteurListSerializer
from .filters import UserProducteurFilter, UserAcheteurFilter
from .models import User 


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


class VerificationCompletudeView(APIView):
    """
    Vérifie la complétude du profil producteur de l'utilisateur connecté. 
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user 
        data = {
            "complet": True,
            "champs_manquants": [],
            "pourcentage_completion": 100
        }

        # Vérification pour producteur physique
        if hasattr(user, 'producteurpersonnephysique'):
            producteur = user.producteurpersonnephysique
            data["type_producteur"] = "physique"
            champs_obligatoires = [
                'experience_agricole', 'certification',
                'adresse', 'ville', 'region', 'pays'
            ]
            
        # Vérification pour producteur organisation
        elif hasattr(user, 'producteurorganisation'):
            producteur = user.producteurorganisation
            data["type_producteur"] = "organisation"
            champs_obligatoires = [
                'raison_sociale', 'type_organisation',
                'nom_dirigeant', 'fonction_dirigeant',
                'adresse', 'ville', 'region', 'pays'
            ]
        else:
            return Response(
                {"detail": "L'utilisateur n'a pas de profil producteur"},
                status=400
            )

        # Vérification des champs
        champs_manquants = []
        for champ in champs_obligatoires:
            if not getattr(producteur, champ):
                champs_manquants.append(champ)

        if champs_manquants:
            data["complet"] = False
            data["champs_manquants"] = champs_manquants
            data["pourcentage_completion"] = int(
                (len(champs_obligatoires) - len(champs_manquants)) / len(champs_obligatoires) * 100)
                
        serializer = CompletudeProducteurSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data) 


class UserProducteurListView(generics.ListAPIView):
    serializer_class = UserProducteurListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = UserProducteurFilter
    
    def get_queryset(self):
        queryset = User.objects.filter(role='PROD').order_by('-date_inscription')
        return queryset

class UserAcheteurListView(generics.ListAPIView):
    """
    Liste des utilisateurs acheteurs avec filtrage et recherche.
    """
    serializer_class = UserAcheteurListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = UserAcheteurFilter
    
    def get_queryset(self):
        queryset = User.objects.filter(role='ACHE').order_by('-date_inscription')
        return queryset