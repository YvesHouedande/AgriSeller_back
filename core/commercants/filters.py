import django_filters
from .models import Commercant
from core.localisation.models import Ville, Region

class CommercantFilter(django_filters.FilterSet):
    type_commercant = django_filters.ChoiceFilter(
        field_name='type_commercant',
        lookup_expr='iexact',
        choices=Commercant.TYPES_COMMERCANT,
        help_text="""
        Type de commerçant:
        - DETAIL: Détaillant
        - GROS: Grossiste  
        - EXPORT: Exportateur
        - IMPORT: Importateur
        """
    )
    ville = django_filters.ModelChoiceFilter(
        field_name='ville',
        queryset=Ville.objects.all()
    )
    region = django_filters.ModelChoiceFilter(
        field_name='ville__region',
        queryset=Region.objects.all()
    )
    actif = django_filters.BooleanFilter()
    date_creation_min = django_filters.DateFilter(
        field_name='date_creation',
        lookup_expr='gte'
    )
    date_creation_max = django_filters.DateFilter(
        field_name='date_creation',
        lookup_expr='lte'
    )

    class Meta:
        model = Commercant
        fields = [
            'type_commercant',
            'ville',
            'region',
            'actif'
        ]