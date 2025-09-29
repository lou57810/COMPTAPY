# from django.test import TestCase

from django.test import TestCase
from django.contrib.auth import get_user_model
from api.utils import create_user_and_entreprise

User = get_user_model()


class CreateUserAndEntrepriseTests(TestCase):

    def test_create_gerant_with_entreprise(self):
        """Un gérant doit être créé avec son entreprise liée"""
        user = create_user_and_entreprise(
            email="gerant@test.com",
            password="testpass123",
            role="GERANT",
            nom="Entreprise GERANT",
            siret="12345678900011",
            ape="6201Z"
        )

        self.assertEqual(user.role, "GERANT")
        self.assertTrue(user.is_owner)
        self.assertIsNotNone(user.entreprise)
        self.assertEqual(user.entreprise.nom, "Entreprise GERANT")

    def test_create_expert_comptable_with_entreprise(self):
        """Un expert-comptable doit aussi avoir son entreprise propre"""
        user = create_user_and_entreprise(
            email="expert@test.com",
            password="testpass123",
            role="EXPERT_COMPTABLE",
            nom="Cabinet EXPERT",
            siret="98765432100022",
            ape="6920Z"
        )

        self.assertEqual(user.role, "EXPERT_COMPTABLE")
        self.assertTrue(user.is_owner)
        self.assertIsNotNone(user.entreprise)
        self.assertEqual(user.entreprise.nom, "Cabinet EXPERT")

