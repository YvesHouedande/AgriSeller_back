import django_filters
from .models import ProducteurPersonnePhysique, ProducteurOrganisation

class ProducteurPhysiqueFilter(django_filters.FilterSet):
    age_min = django_filters.NumberFilter(field_name='date_naissance', lookup_expr='year__gte')
    age_max = django_filters.NumberFilter(field_name='date_naissance', lookup_expr='year__lte')
    
    class Meta:
        model = ProducteurPersonnePhysique
        fields = {
            'certification': ['exact'],
            'ville': ['exact'],
            'ville__region': ['exact'],
            'situation_matrimoniale': ['exact'],
        }

class ProducteurOrganisationFilter(django_filters.FilterSet):
    membres_min = django_filters.NumberFilter(field_name='nombre_membres', lookup_expr='gte')
    membres_max = django_filters.NumberFilter(field_name='nombre_membres', lookup_expr='lte')
    
    class Meta:
        model = ProducteurOrganisation
        fields = {
            'type_organisation': ['exact'],
            'ville': ['exact'],
            'ville__region': ['exact'],
        }