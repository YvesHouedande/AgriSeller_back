from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.localisation import views

router = DefaultRouter()
router.register(r'pays', views.PaysViewSet, basename='pays')
router.register(r'regions', views.RegionViewSet, basename='region')
router.register(r'villes', views.VilleViewSet, basename='ville')

urlpatterns = [
    path('', include(router.urls)),
]