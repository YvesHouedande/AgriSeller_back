from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.accounts.models import User
from core.localisation.models import Ville
from .models import Commercant

class CommercantTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            telephone="+2250102030405", 
            password="testpass123",
            role="COMM"
        )
        self.ville = Ville.objects.create(nom="Abidjan")
        self.commercant_data = {
            "type_commercant": "DETAIL",
            "raison_sociale": "Ma Boutique",
            "adresse": "123 Rue du Commerce",
            "ville": self.ville.id,
            "telephone": "+2250708090102"
        }

    def test_create_commercant(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('commercant-list'),
            data=self.commercant_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(hasattr(self.user, 'commercant'))