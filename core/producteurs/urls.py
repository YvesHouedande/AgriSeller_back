# from rest_framework.routers import DefaultRouter
# from .views import (
#     ProducteurPhysiqueViewSet,
#     ProducteurOrganisationViewSet
# )
# from django.urls import path, include
# # from .views import VerificationCompletudeView

# router = DefaultRouter()
# router.register(r'physique', ProducteurPhysiqueViewSet, basename='producteur-physique')
# router.register(r'organisation', ProducteurOrganisationViewSet, basename='producteur-organisation')

# urlpatterns = [
#     path('', include(router.urls)),
#     # path(
#     #     'verification-completude/',
#     #     VerificationCompletudeView.as_view(),
#     #     name='verification-completude'
#     # ),
# ]


# producteurs/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ProducteurPhysiqueViewSet,
    ProducteurOrganisationViewSet,
    OffreProducteurViewSet,
    ExploitationProducteurViewSet 
)

router = DefaultRouter()
router.register(r'organisation', ProducteurOrganisationViewSet, basename='producteur-organisation')
router.register(r'physique', ProducteurPhysiqueViewSet, basename='producteur-physique')

urlpatterns = [
    path('<str:type>/<uuid:id>/offres/', OffreProducteurViewSet.as_view({'get': 'list'})), 
    path('<str:type>/<uuid:id>/exploitations/', ExploitationProducteurViewSet.as_view({'get': 'list'})),
] + router.urls