# productions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.productions import views

router = DefaultRouter()
router.register(r'categories', views.CategorieCultureViewSet, basename='categorie')
router.register(r'cultures', views.CultureViewSet, basename='culture')
router.register(r'exploitations', views.ExploitationAgricoleViewSet, basename='exploitation')
router.register(r'exploitation-cultures', views.ExploitationCultureViewSet, basename='exploitation-culture')

urlpatterns = [
    path('', include(router.urls)),
]