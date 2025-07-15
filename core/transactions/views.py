from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Offre, MouvementStock, Commande
from .serializers import OffreSerializer, MouvementStockSerializer, CreateOffreSerializer
from core.notifications.services import create_and_send_notification, notify_validators, send_notification_to_user
from core.transactions.permissions import IsClientOrValidateur
from .serializers import CommandeSerializer, UpdateStatutSerializer


class OffreViewSet(viewsets.ModelViewSet):
    queryset = Offre.objects.filter(est_active=True)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOffreSerializer
        return OffreSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Producteurs voient leurs offres
        if hasattr(user, 'producteur_personnephysique'):
            return queryset.filter(producteur_physique=user.producteur_personnephysique)
        elif hasattr(user, 'producteur_organisation'):
            return queryset.filter(producteur_organisation=user.producteur_organisation)
        
        # Validateurs voient toutes les offres non validées
        if user.role == 'VALID':
            return queryset.filter(est_valide=False)
            
        return queryset.none()

    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        offre = self.get_object()
        offre.est_valide = True
        offre.save()
        
        # Notification au producteur
        create_and_send_notification(
            offre.producteur.user,
            'OFFRE_VALIDEE',
            'Offre validée',
            f"Votre offre {offre.nom_produit} a été validée",
            {'offre_id': str(offre.id)}
        )
        
        return Response({'status': 'offre validée'})

    @action(detail=True, methods=['post'])
    def rejeter(self, request, pk=None):
        offre = self.get_object()
        raison = request.data.get('raison', '')
        offre.est_active = False
        offre.save()
        
        # Notification au producteur
        create_and_send_notification(
            offre.producteur.user,
            'OFFRE_REJETEE',
            'Offre rejetée',
            f"Votre offre {offre.nom_produit} a été rejetée. Raison: {raison}",
            {'offre_id': str(offre.id), 'raison': raison}
        )
        
        return Response({'status': 'offre rejetée'})

class MouvementStockViewSet(viewsets.ModelViewSet):
    serializer_class = MouvementStockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MouvementStock.objects.filter(offre__producteur__user=self.request.user)

    def perform_create(self, serializer):
        mouvement = serializer.save(utilisateur=self.request.user)



# class CommandeViewSet(viewsets.ModelViewSet):
#     queryset = Commande.objects.select_related('offre', 'client')
#     serializer_class = CommandeSerializer
#     permission_classes = [IsAuthenticated, IsClientOrValidateur]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         if self.request.user.role == 'CLIENT':
#             return qs.filter(client=self.request.user)
#         return qs

#     def perform_create(self, serializer):
#         commande = serializer.save(client=self.request.user)
#         self._notify_creation(commande)

#     @action(detail=True, methods=['post'], serializer_class=UpdateStatutSerializer)
#     def valider(self, request, pk=None):
#         commande = self.get_object()
#         serializer = self.get_serializer(commande, data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         commande = serializer.save(
#             statut='VALIDEE',
#             validateur=request.user
#         )
#         self._notify_client(commande, 'validée')
#         return Response(serializer.data)

#     @action(detail=True, methods=['post'])
#     def annuler(self, request, pk=None):
#         commande = self.get_object()
#         commande.statut = 'ANNULEE'
#         commande.save()
        
#         if commande.client == request.user:
#             self._notify_validateurs_annulation(commande)
#         return Response({'status': 'annulée'})

#     # Méthodes de notification privées
#     def _notify_creation(self, commande):
#         notify_validators(
#             'COMMANDE_CREEE',
#             f'Nouvelle commande CMD-{commande.id}',
#             f"Client: {commande.client.email} | Produit: {commande.offre.nom_produit}",
#             {'commande_id': commande.id}
#         )

#     def _notify_client(self, commande, action):
#         send_notification_to_user(
#             commande.client.id,
#             {
#                 'type': 'COMMANDE_MAJ',
#                 'title': f'Commande {action}',
#                 'message': f'Votre commande CMD-{commande.id} a été {action}',
#             'metadata': {
#                 'commande_id': str(commande.id),  
#                 'offre_id': str(commande.offre.id) if commande.offre else None
#             }
#             }
#         )

#     def _notify_validateurs_annulation(self, commande):
#         notify_validators(
#             'COMMANDE_ANNULEE',
#             f'Annulation CMD-{commande.id}',
#             f"Annulée par le client: {commande.client.email}",
#             {'commande_id': commande.id}
#         )




class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.select_related(
        'offre',
        'acheteur_physique__user',
        'acheteur_organisation__user',
        'validateur'
    ).prefetch_related(
        'offre__producteur_organisation',
        'offre__producteur_physique'
    )
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrValidateur]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # Si l'utilisateur est un acheteur (physique ou organisation)
        if hasattr(user, 'acheteurpersonnephysique'):
            return qs.filter(acheteur_physique=user.acheteurpersonnephysique)
        elif hasattr(user, 'acheteurorganisation'):
            return qs.filter(acheteur_organisation=user.acheteurorganisation)
        
        # Si l'utilisateur est un validateur ou admin, retourne toutes les commandes
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        acheteur_field = None
        
        # Détermine le type d'acheteur
        if hasattr(user, 'acheteurpersonnephysique'):
            acheteur_field = {'acheteur_physique': user.acheteurpersonnephysique}
        elif hasattr(user, 'acheteurorganisation'):
            acheteur_field = {'acheteur_organisation': user.acheteurorganisation}
        
        if acheteur_field is None:
            raise serializers.ValidationError("Seuls les acheteurs peuvent créer des commandes")
        
        commande = serializer.save(**acheteur_field)
        self._notify_creation(commande)

    @action(detail=True, methods=['post'], serializer_class=UpdateStatutSerializer)
    def valider(self, request, pk=None):
        commande = self.get_object()
        serializer = self.get_serializer(commande, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        commande = serializer.save(
            statut='VALIDEE',
            validateur=request.user
        )
        self._notify_client(commande, 'validée')
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        commande = self.get_object()
        commande.statut = 'ANNULEE'
        commande.save()
        
        if self._is_acheteur(commande, request.user):
            self._notify_validateurs_annulation(commande)
        return Response({'status': 'annulée'})

    # Méthodes utilitaires privées
    def _is_acheteur(self, commande, user):
        """Vérifie si l'utilisateur est l'acheteur de la commande"""
        return (
            (commande.acheteur_physique and hasattr(user, 'acheteurpersonnephysique') and 
            (commande.acheteur_physique == user.acheteurpersonnephysique)
        ) or (
            (commande.acheteur_organisation and hasattr(user, 'acheteurorganisation') and 
            (commande.acheteur_organisation == user.acheteurorganisation)
        )
        ))
    def _get_acheteur_email(self, commande):
        """Récupère l'email de l'acheteur"""
        if commande.acheteur_physique:
            return commande.acheteur_physique.user.email
        elif commande.acheteur_organisation:
            return commande.acheteur_organisation.user.email
        return None

    # Méthodes de notification
    def _notify_creation(self, commande):
        notify_validators(
            'COMMANDE_CREEE',
            f'Nouvelle commande CMD-{commande.id}',
            f"Produit: {commande.offre.nom_produit}",
            {
                'commande_id': str(commande.id),
                'acheteur_type': 'physique' if commande.acheteur_physique else 'organisation'
            }
        )

    def _notify_client(self, commande, action):
        email = self._get_acheteur_email(commande)
        if not email:
            return
            
        send_notification_to_user(
            commande.acheteur_physique.user.id if commande.acheteur_physique else commande.acheteur_organisation.user.id,
            {
                'type': 'COMMANDE_MAJ',
                'title': f'Commande {action}',
                'message': f'Votre commande CMD-{commande.id} a été {action}',
                'metadata': {
                    'commande_id': str(commande.id),
                    'offre_id': str(commande.offre.id) if commande.offre else None
                }
            }
        )

    def _notify_validateurs_annulation(self, commande):
        email = self._get_acheteur_email(commande)
        if not email:
            return
            
        notify_validators(
            'COMMANDE_ANNULEE',
            f'Annulation CMD-{commande.id}',
            f"Produit: {commande.offre.nom_produit}",
            {
                'commande_id': str(commande.id),
                'acheteur_type': 'physique' if commande.acheteur_physique else 'organisation'
            }
        )

