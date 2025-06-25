# transactions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.transactions import views

router = DefaultRouter()
router.register(r'offres', views.OffreViewSet, basename='offre')
router.register(r'commandes', views.CommandeViewSet, basename='commande')
router.register(r'propositions', views.PropositionProducteurViewSet, basename='proposition')

urlpatterns = [
    path('', include(router.urls)),
    path('mouvements/', views.MouvementStockViewSet.as_view({'get': 'list'}), name='mouvement-list'),
]