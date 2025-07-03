# core/commercants/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AcheteurPersonnePhysiqueViewSet,
    AcheteurOrganisationViewSet,
)

router = DefaultRouter()
router.register(r'personnes-physiques', AcheteurPersonnePhysiqueViewSet, basename='acheteur-personne-physique')
router.register(r'organisations', AcheteurOrganisationViewSet, basename='acheteur-organisation')

urlpatterns = [
    path('', include(router.urls)),
]