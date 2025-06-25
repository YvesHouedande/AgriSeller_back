# localisation/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.localisation.models import Pays, Region, Ville
from core.localisation.serializers import (
    PaysSerializer,
    RegionSerializer,
    VilleSerializer,
    VilleDetailSerializer
)

class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'code_iso']
    ordering_fields = ['nom', 'code_iso']
    ordering = ['nom']

class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['pays']
    search_fields = ['nom', 'code']

    def get_queryset(self):
        queryset = Region.objects.all()
        pays_id = self.request.query_params.get('pays')
        if pays_id:
            queryset = queryset.filter(pays__id=pays_id)
        return queryset

class VilleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region']
    search_fields = ['nom', 'code_postal']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return VilleDetailSerializer
        return VilleSerializer

    def get_queryset(self):
        queryset = Ville.objects.all()
        region_id = self.request.query_params.get('region')
        if region_id:
            queryset = queryset.filter(region__id=region_id)
        return queryset