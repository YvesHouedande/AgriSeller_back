import django_filters
from django.db import models
from .models import User  

class UserProducteurFilter(django_filters.FilterSet):
    role = django_filters.CharFilter(field_name='role', lookup_expr='iexact')
    is_verified = django_filters.BooleanFilter(field_name='is_verified')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    search = django_filters.CharFilter(method='filter_search')
    certification = django_filters.CharFilter(method='filter_certification')
    type_organisation = django_filters.CharFilter(field_name='producteurorganisation__type_organisation', lookup_expr='iexact')

    
    # Modification ici pour les ForeignKey
    pays = django_filters.UUIDFilter(method='filter_pays')
    region = django_filters.UUIDFilter(method='filter_region')
    ville = django_filters.UUIDFilter(method='filter_ville')

    class Meta:
        model = User
        fields = ['role', 'is_verified', 'is_active']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(telephone__icontains=value) |
            models.Q(email__icontains=value) |
            models.Q(first_name__icontains=value) |
            models.Q(last_name__icontains=value) |
            models.Q(producteurorganisation__adresse__icontains=value) |
            models.Q(producteurpersonnephysique__adresse__icontains=value)
        )

    def filter_ville(self, queryset, name, value):
        return queryset.filter(
            models.Q(producteurorganisation__ville_id=value) |
            models.Q(producteurpersonnephysique__ville_id=value)
        )

    def filter_region(self, queryset, name, value):
        return queryset.filter(
            models.Q(producteurorganisation__region_id=value) |
            models.Q(producteurpersonnephysique__region_id=value)
        )

    def filter_pays(self, queryset, name, value):
        return queryset.filter(
            models.Q(producteurorganisation__pays_id=value) |
            models.Q(producteurpersonnephysique__pays_id=value)
        )
    
    def filter_certification(self, queryset, name, value):
        return queryset.filter(
            models.Q(producteurorganisation__certification__iexact=value) |
            models.Q(producteurpersonnephysique__certification__iexact=value)
        )

    def filter_type_organisation(self, queryset, name, value):
        return queryset.filter(
            producteurorganisation__type_organisation__iexact=value
        )


class UserAcheteurFilter(django_filters.FilterSet):
    is_verified = django_filters.BooleanFilter(field_name='is_verified')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    search = django_filters.CharFilter(method='filter_search')
    pays = django_filters.UUIDFilter(method='filter_pays')
    region = django_filters.UUIDFilter(method='filter_region')
    ville = django_filters.UUIDFilter(method='filter_ville')
    type_commerce = django_filters.CharFilter(method='filter_type_commerce')
    forme_juridique = django_filters.CharFilter(field_name='acheteurorganisation__forme_juridique', lookup_expr='iexact')
    acheteur_type = django_filters.CharFilter(method='filter_acheteur_type')

    class Meta:
        model = User
        fields = ['is_verified', 'is_active']

    def filter_ville(self, queryset, name, value):
        return queryset.filter(
            models.Q(acheteurorganisation__ville_id=value) |
            models.Q(acheteurpersonnephysique__ville_id=value)
        )

    def filter_region(self, queryset, name, value):
        return queryset.filter(
            models.Q(acheteurorganisation__region_id=value) |
            models.Q(acheteurpersonnephysique__region_id=value)
        )

    def filter_pays(self, queryset, name, value):
        print(dir(User))
        return queryset.filter(
            models.Q(acheteurorganisation__pays_id=value) |
            models.Q(acheteurpersonnephysique__pays_id=value)
        )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(telephone__icontains=value) |
            models.Q(email__icontains=value) |
            models.Q(first_name__icontains=value) |
            models.Q(last_name__icontains=value) |
            models.Q(acheteurorganisation__raison_sociale__icontains=value) 
        )

    def filter_type_commerce(self, queryset, name, value):
        return queryset.filter(
            models.Q(acheteurorganisation__type_commerce__iexact=value) |
            models.Q(acheteurpersonnephysique__type_commerce__iexact=value)
        )

    def filter_acheteur_type(self, queryset, name, value):
        """Filtre par type d'acheteur (physique/organisation)"""
        if value == 'physique':
            return queryset.filter(acheteurpersonnephysique__isnull=False)
        elif value == 'organisation':
            return queryset.filter(acheteurorganisation__isnull=False)
        return queryset