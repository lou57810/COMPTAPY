from django.test import TestCase
from django.contrib.auth import get_user_model
from api.utils import create_user_and_entreprise
from django.urls import reverse


User = get_user_model()


class LoginViewTests(TestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "password123"
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            role="GERANT"
        )


class UtilsTests(TestCase):
    def test_create_gerant(self):
        user, entreprise = create_user_and_entreprise(
            email="gerant@test.com",
            password="password123",
            role="GERANT",
            nom="Entreprise Gerant"
        )
        self.assertEqual(user.role, "GERANT")
        self.assertEqual(user.entreprise, entreprise)
        self.assertTrue(entreprise.nom, "Entreprise Gerant")


class AuthenticationTests(TestCase):

    def setUp(self):
        # On crée un utilisateur pour les tests
        self.email = "gerant@test.com"
        self.password = "testpass123"
        self.user = create_user_and_entreprise(
            email=self.email,
            password=self.password,
            role="GERANT",
            nom="Entreprise GERANT",
            siret="12345678900011",
            ape="6201Z"
        )
"""
def test_login_with_email_and_password(self):
    # Un utilisateur doit pouvoir se connecter avec email + mot de passe
    login_success = self.client.login(email=self.email, password=self.password)
    self.assertTrue(login_success)

    def test_login_with_email_and_password(self):
        # Un utilisateur doit pouvoir se connecter avec email + mot de passe
        login_success = self.client.login(email=self.email, password=self.password)
        self.assertTrue(login_success)


def test_login_view_redirects_after_success(self):
    # La vue de login doit rediriger vers l'accueil après connexion réussie
    response = self.client.post(reverse("login"), {
        "email": self.email,
        "password": self.password
    })
    self.assertEqual(response.status_code, 302)  # redirection
    self.assertEqual(response.url, reverse("accueil"))

class CreateUserAndEntrepriseTests(TestCase):

    def test_create_gerant_with_entreprise(self):
        # Un gérant doit être créé avec son entreprise liée
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
        # Un expert-comptable doit aussi avoir son entreprise propre
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
"""

"""
def test_login_view_redirects_after_success(self):
    # La vue de login doit rediriger vers l'accueil après connexion réussie
    response = self.client.post(reverse("login"), {
        "email": self.email,
        "password": self.password
    })
    self.assertEqual(response.status_code, 302)  # redirection
    self.assertEqual(response.url, reverse("accueil"))
"""
