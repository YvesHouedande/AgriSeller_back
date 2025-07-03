# Lancer les conteneurs
docker compose up --build 

# Lancer uniquement les tests unitaires
pytest core/accounts/tests/test_serializers.py -v

# Lancer uniquement les tests d'intégration
pytest core/accounts/tests/test_auth_flows.py -v

# Lancer avec couverture
pytest --cov=core.accounts --cov-report=html

# Accéder au bash du connteneur backend
docker-compose exec web bash

# Adrresse websoket( connexion)
ws://localhost:8000/ws/notifications/?token=<token_utilisateur>
