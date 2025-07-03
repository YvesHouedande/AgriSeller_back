from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    CategorieCulture,
    Culture,
    ExploitationAgricole,
    ExploitationCulture
)
from .serializers import (
    CategorieCultureSerializer,
    CultureSerializer,
    ExploitationAgricoleSerializer,
    ExploitationCultureSerializer
)
from .filters import CultureFilter, ExploitationFilter

class CategorieCultureViewSet(viewsets.ModelViewSet):
    queryset = CategorieCulture.objects.all()
    serializer_class = CategorieCultureSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'description']

class CultureViewSet(viewsets.ModelViewSet):
    queryset = Culture.objects.filter(active=True)
    serializer_class = CultureSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CultureFilter
    search_fields = ['nom', 'nom_scientifique']

class ExploitationAgricoleViewSet(viewsets.ModelViewSet):
    serializer_class = ExploitationAgricoleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ExploitationFilter
    search_fields = ['nom', 'adresse']

    def get_queryset(self):
        user = self.request.user
        queryset = ExploitationAgricole.objects.all()
        
        if hasattr(user, 'producteur_personnephysique'):
            return queryset.filter(producteur_physique=user.producteur_personnephysique)
        elif hasattr(user, 'producteur_organisation'):
            return queryset.filter(producteur_organisation=user.producteur_organisation)
        
        return queryset.none()

class ExploitationCultureViewSet(viewsets.ModelViewSet):
    serializer_class = ExploitationCultureSerializer

    def get_queryset(self):
        exploitation_id = self.request.query_params.get('exploitation')
        if exploitation_id:
            return ExploitationCulture.objects.filter(exploitation_id=exploitation_id)
        return ExploitationCulture.objects.none()