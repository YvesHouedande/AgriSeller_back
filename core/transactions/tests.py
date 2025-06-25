# transactions/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.accounts.models import User
from core.transactions.models import Offre, Commande

class OffreAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.producteur = User.objects.create_user(username='producteur', password='prodpass')
        # Créer des producteurs selon vos modèles

    def test_list_offres_unauthenticated(self):
        response = self.client.get(reverse('offre-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_offre_authenticated(self):
        self.client.force_authenticate(user=self.producteur)
        data = {
            'nom_produit': 'Test produit',
            'culture': 1,  # ID d'une culture existante
            'quantite_initiale': 100,
            'prix_unitaire': 10.50,
            # ... autres champs nécessaires
        }
        response = self.client.post(reverse('offre-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CommandeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='client', password='clientpass')
        # Créer une offre de test

    def test_create_commande(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'offre': 1,  # ID d'une offre existante
            'quantite': 5,
        }
        response = self.client.post(reverse('commande-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)