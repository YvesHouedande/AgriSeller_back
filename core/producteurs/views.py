from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.accounts.models import User
from .models import ProducteurPersonnePhysique, ProducteurOrganisation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet 
from .serializers import (
    ProducteurPhysiqueSerializer,
    ProducteurOrganisationSerializer,
    ProducteurPhysiqueDetailSerializer,
    ProducteurOrganisationDetailSerializer
)
from core.transactions.models import Offre
from core.productions.models import ExploitationAgricole
from core.productions.serializers import ExploitationAgricoleSerializer 
from core.transactions.serializers import OffreSerializer

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

class OffreProducteurViewSet(ListModelMixin, GenericViewSet):
    serializer_class = OffreSerializer  
    
    def get_queryset(self):
        producteur_id = self.kwargs['id']
        producteur_type = self.kwargs['type']
        
        if producteur_type == 'organisation':
            return Offre.objects.filter(
                producteur_organisation_id=producteur_id,
                est_active=True
            ).select_related('culture', 'lieu_retrait')
        else:
            return Offre.objects.filter(
                producteur_physique_id=producteur_id,
                est_active=True
            ).select_related('culture', 'lieu_retrait')

class ExploitationProducteurViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ExploitationAgricoleSerializer   
    
    def get_queryset(self):
        producteur_id = self.kwargs['id']
        producteur_type = self.kwargs['type']
        
        if producteur_type == 'organisation':
            return ExploitationAgricole.objects.filter(
                producteur_organisation_id=producteur_id
            ).prefetch_related('cultures_plantees__culture')
        else:
            return ExploitationAgricole.objects.filter(
                producteur_physique_id=producteur_id
            ).prefetch_related('cultures_plantees__culture')
