
# from rest_framework import permissions

# class IsClientOrValidateur(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.client == request.user or request.user.role == 'VALID'

from rest_framework import permissions

class IsClientOrValidateur(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Vérifie si l'utilisateur est un validateur ou admin
        # if request.user.role in ['VALID', 'ADMIN']:
        #     return True
            
        # Vérifie si l'utilisateur est l'acheteur de la commande
        if hasattr(request.user, 'acheteurpersonnephysique'):
            return obj.acheteur_physique == request.user.acheteurpersonnephysique
        elif hasattr(request.user, 'acheteurorganisation'):
            return obj.acheteur_organisation == request.user.acheteurorganisation
            
        return False