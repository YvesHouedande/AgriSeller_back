# transactions/permissions.py
from rest_framework import permissions

class IsProducteurOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(request.user, 'producteur_personnephysique') or hasattr(request.user, 'producteur_organisation')

class IsClientOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return not (hasattr(request.user, 'producteur_personnephysique') or hasattr(request.user, 'producteur_organisation'))