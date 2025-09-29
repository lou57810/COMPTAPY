from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from api.models import Entreprise, CompteComptable

User = get_user_model()

class SetupViewTest(TestCase):
    def test_setup_creates_owner_and_entreprise(self):
        # Vérifie qu'aucune entreprise n'existe au départ
        self.assertEqual(Entreprise.objects.count(), 0)

        # Données POST simulant le formulaire setup
        post_data = {
            "nom": "Test_Compta",
            "siret": "12345678900011",
            "ape": "6201Z",
            "adresse": "1 rue de la Paix",
            "date_creation": "2025-09-14",
            "email": "gerant@example.com",
            "password": "motdepassefort123",
        }

        response = self.client.post(reverse("setup"), data=post_data)
        # Après setup, on s'attend à une redirection vers "login"
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

        # Vérifie qu'une entreprise a bien été créée
        entreprise = Entreprise.objects.first()
        self.assertIsNotNone(entreprise)
        self.assertEqual(entreprise.nom, "Test_Compta")

        # Vérifie que l'utilisateur OWNER a été créé
        user = User.objects.first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "gerant@example.com")
        self.assertTrue(user.check_password("motdepassefort123"))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_owner)
        self.assertEqual(user.role, "OWNER")

        # Vérifie que l'utilisateur est bien lié à l'entreprise
        self.assertEqual(user.entreprise, entreprise)
        self.assertEqual(entreprise.owner, user)

        # Vérifie que les comptes PGC ont bien été clonés pour cette entreprise
        comptes = CompteComptable.objects.filter(entreprise=entreprise)
        self.assertGreater(comptes.count(), 0, "Le PGC n'a pas été cloné pour l'entreprise")

