from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter
)

LOGIN_DOCS = extend_schema(
    tags=['Authentification'],
    summary="Connexion des utilisateurs",
    description="Endpoint pour connecter les producteurs et commerçants. Retourne des tokens JWT.",
    examples=[
        OpenApiExample(
            "Producteur Sénégalais",
            value={"telephone": "+221781234567", "password": "PassAgri123"},
            request_only=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Connexion réussie",
            examples=[
                OpenApiExample(
                    "Réponse succès",
                    value={
                        "access": "xxx.yyy.zzz",
                        "refresh": "aaa.bbb.ccc"
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Identifiants invalides",
            examples=[
                OpenApiExample(
                    "Exemple d'erreur",
                    value={
                        "error": "Identifiants invalides",
                        "details": {
                            "telephone": ["Ce champ est obligatoire"],
                            "password": ["Ce champ est obligatoire"]
                        }
                    }
                )
            ]
        )
    }
)

REGISTER_DOCS = extend_schema(
    tags=['Authentification'],
    summary="Enregistrement des utilisateurs",
    description="""Endpoint pour créer un nouveau compte et obtenir immédiatement les tokens JWT.
    **Rôles disponibles** :
    - PROD : Producteur agricole
    - COMM : Commerçant""",
    examples=[
        OpenApiExample(
            "Enregistrement Producteur",
            value={
                "telephone": "+221781234567",
                "password": "PassAgri123",
                "role": "PROD"
            },
            request_only=True
        )
    ],
    responses={
        201: OpenApiResponse(
            description="Compte créé avec tokens JWT",
            examples=[
                OpenApiExample(
                    "Réponse succès",
                    value={
                        "access": "xxx.yyy.zzz",
                        "refresh": "aaa.bbb.ccc"
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Données invalides",
            examples=[
                OpenApiExample(
                    "Numéro existant",
                    value={
                        "error": "Erreur de validation",
                        "details": {
                            "telephone": ["Ce numéro est déjà utilisé"]
                        }
                    }
                ),
                OpenApiExample(
                    "Données manquantes",
                    value={
                        "error": "Erreur de validation",
                        "details": {
                            "password": ["Ce champ est obligatoire"],
                            "role": ["Ce champ est obligatoire"]
                        }
                    }
                )
            ]
        ),
        500: OpenApiResponse(
            description="Erreur serveur",
            examples=[
                OpenApiExample(
                    "Erreur inattendue",
                    value={
                        "error": "Erreur lors de la création du compte",
                        "details": "Message d'erreur technique"
                    }
                )
            ]
        )
    }
)