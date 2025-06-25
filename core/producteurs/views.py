from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.accounts.models import User
from .models import ProducteurPersonnePhysique, ProducteurOrganisation
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CompletudeProducteurSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ProducteurPhysiqueSerializer,
    ProducteurOrganisationSerializer,
    ProducteurPhysiqueDetailSerializer,
    ProducteurOrganisationDetailSerializer
)

class ProducteurPhysiqueViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les opérations CRUD sur les producteurs personnes physiques.
    Permet de filtrer par : certification, ville, region, age_min, age_max
    Permet de rechercher par : nom, prénom, numéro CNI
    """
    queryset = ProducteurPersonnePhysique.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'certification': ['exact'],
        'ville': ['exact'],
        'ville__region': ['exact'],
        'date_naissance': ['year__gte', 'year__lte'],
    }
    search_fields = [
        'user__first_name',
        'user__last_name',
        'numero_cni',
    ]
    ordering_fields = ['user__last_name', 'experience_agricole', 'date_creation']
    ordering = ['user__last_name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProducteurPhysiqueDetailSerializer
        return ProducteurPhysiqueSerializer

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'producteur_personnephysique'):
            raise serializers.ValidationError("Cet utilisateur a déjà un profil producteur")
        serializer.save(user=self.request.user)

class ProducteurOrganisationViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les opérations CRUD sur les producteurs organisations.
    Permet de filtrer par : type_organisation, ville, region
    Permet de rechercher par : raison_sociale, numéro registre
    """
    queryset = ProducteurOrganisation.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'type_organisation': ['exact'],
        'ville': ['exact'],
        'ville__region': ['exact'],
    }
    search_fields = [
        'raison_sociale',
        'numero_registre',
        'nom_dirigeant',
    ]
    ordering_fields = ['raison_sociale', 'date_creation', 'nombre_membres']
    ordering = ['raison_sociale']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProducteurOrganisationDetailSerializer
        return ProducteurOrganisationSerializer

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'producteur_organisation'):
            raise serializers.ValidationError("Cet utilisateur a déjà un profil organisation")
        serializer.save(user=self.request.user)


class VerificationCompletudeView(APIView):
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