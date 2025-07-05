# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import action
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
# from .filters import CommercantFilter
# from .models import Commercant
# from .serializers import (
#     CommercantSerializer,
#     CreateCommercantSerializer,
#     CompletudeCommercantSerializer
# )

# class CommercantViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint pour la gestion des commerçants.

#     Permet les opérations CRUD sur les profils des commerçants avec :
#     - Filtrage avancé par type, région, ville, etc.
#     - Recherche full-text
#     - Tri personnalisé
#     - Pagination
#     - Vérification de la complétude du profil
#     """
#     queryset = Commercant.objects.filter(actif=True)
#     permission_classes = [IsAuthenticated]
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter
#     ]
#     filterset_class = CommercantFilter
#     search_fields = [
#         'raison_sociale',
#         'numero_registre',
#         'user__telephone',
#         'ville__nom',
#         'ville__region__nom'
#     ]
#     ordering_fields = [
#         'raison_sociale',
#         'date_creation',
#         'type_commercant'
#     ]
#     ordering = ['-date_creation']

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return CreateCommercantSerializer
#         return CommercantSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset()
        
#         # Pour les commercants normaux: seulement leur profil
#         if hasattr(self.request.user, 'commercant'):
#             if self.request.user.role == 'COMM':
#                 return queryset.filter(user=self.request.user)
        
#         # Pour les admins/validateurs: accès complet avec filtres
#         return queryset

#     @action(detail=False, methods=['get'])
#     def verification_completude(self, request):
#         commercant = getattr(request.user, 'commercant', None)
        
#         if not commercant:
#             return Response(
#                 {"detail": "L'utilisateur n'a pas de profil commerçant"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         champs_obligatoires = [
#             'type_commercant', 'raison_sociale',
#             'adresse', 'ville', 'telephone'
#         ]
        
#         champs_manquants = [
#             champ for champ in champs_obligatoires 
#             if not getattr(commercant, champ)
#         ]
        
#         data = {
#             "complet": len(champs_manquants) == 0,
#             "champs_manquants": champs_manquants,
#             "pourcentage_completion": int(
#                 (len(champs_obligatoires) - len(champs_manquants)) / 
#                 len(champs_obligatoires) * 100)
#         }
        
#         serializer = CompletudeCommercantSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data)


# core/commercants/views.py
from rest_framework import viewsets
from .models import AcheteurPersonnePhysique, AcheteurOrganisation
from .serializers import (
    AcheteurPersonnePhysiqueSerializer, 
    AcheteurOrganisationSerializer
)
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from core.transactions.models import Commande
from core.transactions.serializers import CommandeSerializer

class AcheteurPersonnePhysiqueViewSet(viewsets.ModelViewSet):
    queryset = AcheteurPersonnePhysique.objects.all()
    serializer_class = AcheteurPersonnePhysiqueSerializer
    filterset_fields = {
        'type_commerce': ['exact'],
        'ville__id': ['exact'],
        'actif': ['exact'],
        'date_creation': ['gte', 'lte'],
    }

class AcheteurOrganisationViewSet(viewsets.ModelViewSet):
    queryset = AcheteurOrganisation.objects.all()
    serializer_class = AcheteurOrganisationSerializer
    filterset_fields = {
        'type_commerce': ['exact'],
        'forme_juridique': ['exact'],
        'ville__id': ['exact'],
        'actif': ['exact'],
        'date_creation': ['gte', 'lte'],
    }


class CommandeAcheteurViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CommandeSerializer  
    
    def get_queryset(self):
        acheteur_id = self.kwargs['id']
        acheteur_type = self.kwargs['type']
        
        queryset = Commande.objects.select_related(
            'offre',
            'offre__culture',
            'offre__lieu_retrait',
            'validateur'
        ).prefetch_related(
            'offre__producteur_organisation',
            'offre__producteur_physique'
        ).order_by('-date_creation')
        
        if acheteur_type == 'organisation':
            return queryset.filter(acheteur_organisation_id=acheteur_id)
        else:
            return queryset.filter(acheteur_physique_id=acheteur_id)