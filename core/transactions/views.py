from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.transactions.models import Offre, MouvementStock, Commande, PropositionProducteur
from core.transactions.serializers import (
    OffreSerializer, 
    MouvementStockSerializer,
    CommandeSerializer,
    PropositionProducteurSerializer
)
from core.accounts.models import User
from django.shortcuts import get_object_or_404

class OffreViewSet(viewsets.ModelViewSet):
    queryset = Offre.objects.filter(est_active=True)
    serializer_class = OffreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            producteur_physique=self.request.user.producteur_personnephysique,
            producteur_organisation=self.request.user.producteur_organisation
        )

    @action(detail=True, methods=['post'])
    def ajuster_stock(self, request, pk=None):
        offre = self.get_object()
        quantite = request.data.get('quantite')
        notes = request.data.get('notes', '')

        mouvement = MouvementStock.objects.create(
            offre=offre,
            type_mouvement='AJUSTEMENT',
            quantite=quantite,
            utilisateur=request.user,
            notes=notes
        )

        return Response({
            'status': 'stock ajusté',
            'quantite_actuelle': offre.quantite_actuelle
        })

class CommandeViewSet(viewsets.ModelViewSet):
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Commande.objects.filter(client=user).order_by('-date_commande')

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        commande = self.get_object()
        if commande.client != request.user:
            return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
        
        commande.statut = 'ANNULEE'
        commande.save()
        return Response({'status': 'commande annulée'})

class PropositionProducteurViewSet(viewsets.ModelViewSet):
    serializer_class = PropositionProducteurSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PropositionProducteur.objects.filter(
            commande__client=user
        ).order_by('-commande__date_commande')

    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        proposition = self.get_object()
        # Logique de validation complexe à implémenter
        return Response({'status': 'validé'})