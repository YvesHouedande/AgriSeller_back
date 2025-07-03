from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategorieCultureViewSet,
    CultureViewSet,
    ExploitationAgricoleViewSet,
    ExploitationCultureViewSet
)

router = DefaultRouter()
router.register(r'categories', CategorieCultureViewSet, basename='categorie-culture')
router.register(r'cultures', CultureViewSet, basename='culture')
router.register(r'exploitations', ExploitationAgricoleViewSet, basename='exploitation-agricole')
router.register(r'exploitation-cultures', ExploitationCultureViewSet, basename='exploitation-culture') 

urlpatterns = [
    path('', include(router.urls)),
]