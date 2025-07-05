# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

# # Configuration personnalisée pour l'affichage dans l'admin
# class CustomUserAdmin(UserAdmin):
#     list_display = ('id','telephone', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_staff') 
#     list_filter = ('role', 'is_verified', 'is_staff', 'is_superuser')
#     search_fields = ('telephone', 'email', 'first_name', 'last_name')
#     ordering = ('-date_inscription',)
    
#     fieldsets = (
#         (None, {'fields': ('password',)}),
#         ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'telephone', 'photo_profil')}),
#         ('Rôles et permissions', {
#             'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         # ('Dates importantes', {'fields': ('last_login', 'date_inscription', 'date_mise_a_jour')}), 
#     )

# # Enregistre ton modèle User avec la configuration personnalisée
# admin.site.register(User, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'telephone', 'email', 'role', 'is_verified', 'is_staff', 'date_inscription', 'last_login') 
    list_filter = ('role', 'is_verified', 'is_staff', 'is_superuser')
    search_fields = ('telephone', 'email', 'first_name', 'last_name', 'id')
    ordering = ('-date_inscription',)
    readonly_fields = ('id', 'date_inscription', 'last_login', 'date_mise_a_jour')
    
    fieldsets = (
        (None, {'fields': ('id', 'password')}),
        ('Informations personnelles', {
            'fields': (
                'first_name', 
                'last_name', 
                'email', 
                'telephone', 
                'photo_profil',
                
            )
        }),
        ('Rôles et permissions', {
            'fields': (
                'role', 
                'is_verified', 
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
            ),
        }),
        ('Dates importantes', {
            'fields': (
                'last_login', 
                'date_inscription', 
                'date_mise_a_jour'
            )
        }), 
    )


admin.site.register(User, CustomUserAdmin)