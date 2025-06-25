from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.accounts.models import User

class CompletudeProducteurTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(telephone="+2250102030405", password="testpass123", role="PROD")
        self.client.force_authenticate(user=self.user)

    def test_verification_completude_sans_profil(self):
        response = self.client.get('/api/producteurs/verification-completude/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Ajoutez d'autres tests pour les cas physique/organisation complet/incomplet