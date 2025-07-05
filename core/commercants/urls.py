# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    AcheteurPersonnePhysiqueViewSet,
    AcheteurOrganisationViewSet,
    CommandeAcheteurViewSet
)
from django.urls import path, include 

router = DefaultRouter()
router.register(r'personnes-physiques', AcheteurPersonnePhysiqueViewSet, basename='acheteur-personne-physique')
router.register(r'organisations', AcheteurOrganisationViewSet, basename='acheteur-organisation')

urlpatterns = [
    path('<str:type>/<uuid:id>/commandes/', CommandeAcheteurViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
]