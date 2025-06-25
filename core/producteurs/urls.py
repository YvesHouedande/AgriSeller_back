from rest_framework.routers import DefaultRouter
from .views import (
    ProducteurPhysiqueViewSet,
    ProducteurOrganisationViewSet
)
from django.urls import path, include
from .views import VerificationCompletudeView

router = DefaultRouter()
router.register(r'physique', ProducteurPhysiqueViewSet, basename='producteur-physique')
router.register(r'organisation', ProducteurOrganisationViewSet, basename='producteur-organisation')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'verification-completude/',
        VerificationCompletudeView.as_view(),
        name='verification-completude'
    ),
]