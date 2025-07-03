import django_filters
from core.productions.models import Culture, ExploitationAgricole

class CultureFilter(django_filters.FilterSet):
    categorie = django_filters.CharFilter(field_name='categorie__nom')
    region = django_filters.CharFilter(field_name='regions__nom')
    saison = django_filters.CharFilter(field_name='saison_plantation')
    
    class Meta:
        model = Culture
        fields = ['categorie', 'region', 'saison', 'duree_cycle']

class ExploitationFilter(django_filters.FilterSet):
    statut = django_filters.CharFilter(field_name='statut')
    type_propriete = django_filters.CharFilter(field_name='type_propriete')
    min_superficie = django_filters.NumberFilter(field_name='superficie', lookup_expr='gte')
    max_superficie = django_filters.NumberFilter(field_name='superficie', lookup_expr='lte')
    
    class Meta:
        model = ExploitationAgricole
        fields = ['statut', 'type_propriete', 'min_superficie', 'max_superficie']