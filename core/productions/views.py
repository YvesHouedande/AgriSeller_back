# productions/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.productions.models import (
    CategorieCulture,
    Culture,
    ExploitationAgricole,
    ExploitationCulture
)
from core.productions.serializers import (
    CategorieCultureSerializer,
    CultureSerializer,
    ExploitationAgricoleSerializer,
    ExploitationCultureSerializer
)
from core.productions.filters import CultureFilter, ExploitationFilter

class CategorieCultureViewSet(viewsets.ModelViewSet):
    queryset = CategorieCulture.objects.all()
    serializer_class = CategorieCultureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'description']

class CultureViewSet(viewsets.ModelViewSet):
    queryset = Culture.objects.filter(active=True)
    serializer_class = CultureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CultureFilter
    search_fields = ['nom', 'nom_scientifique']

class ExploitationAgricoleViewSet(viewsets.ModelViewSet):
    serializer_class = ExploitationAgricoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ExploitationFilter
    search_fields = ['nom', 'adresse']

    def get_queryset(self):
        user = self.request.user
        # Filtrer selon le type de producteur
        if hasattr(user, 'producteur_personnephysique'):
            return ExploitationAgricole.objects.filter(producteur_physique=user.producteur_personnephysique)
        elif hasattr(user, 'producteur_organisation'):
            return ExploitationAgricole.objects.filter(producteur_organisation=user.producteur_organisation)
        return ExploitationAgricole.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'producteur_personnephysique'):
            serializer.save(producteur_physique=user.producteur_personnephysique)
        elif hasattr(user, 'producteur_organisation'):
            serializer.save(producteur_organisation=user.producteur_organisation)

class ExploitationCultureViewSet(viewsets.ModelViewSet):
    serializer_class = ExploitationCultureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        # Filtrer selon les exploitations du producteur
        if hasattr(user, 'producteur_personnephysique'):
            return ExploitationCulture.objects.filter(
                exploitation__producteur_physique=user.producteur_personnephysique
            )
        elif hasattr(user, 'producteur_organisation'):
            return ExploitationCulture.objects.filter(
                exploitation__producteur_organisation=user.producteur_organisation
            )
        return ExploitationCulture.objects.none()