from django.contrib import admin
from django.urls import path, include 
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('api/accounts/', include('core.accounts.urls')),

    # Localisation
    path('api/localisation/', include('core.localisation.urls')),
    
    # Producteurs
    path('api/producteurs/', include('core.producteurs.urls')),

    # Commercants
    path('api/commercants/', include('core.commercants.urls')),

    # Productions
    path('api/productions/', include('core.productions.urls')),

    # Transactions
    path('api/transactions/', include('core.transactions.urls')), 

    # Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
