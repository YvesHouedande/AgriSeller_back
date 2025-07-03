from django.urls import path
from .views import (
    LoginView, 
    RegisterView,
    VerificationCompletudeView,
    UserProducteurListView,
    UserAcheteurListView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'), 
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('users/producteurs', UserProducteurListView.as_view(), name='user-list'), 
    path('users/acheteurs', UserAcheteurListView.as_view(), name='user-acheteur-list'),

    # Endpoint pour vérifier la complétude du profil producteur
    path(
        'verification-completude/',
        VerificationCompletudeView.as_view(),
        name='verification-completude'
    ),
] 