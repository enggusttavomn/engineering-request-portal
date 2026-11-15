"""
Testes unitários da app de accounts (contas/usuários).

Este arquivo contém testes para:
- Modelos de usuário e perfil
- Autenticação
- Formulários de login
- Views de login e dashboards

Para executar os testes:
    python manage.py test accounts
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.directory import USER_DIRECTORY_MAP
from seed_users import seed_demo_users


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("demo", password="local-test-password")
        self.user.groups.add(Group.objects.create(name="SOLICITANTE"))

    def test_user_profile_is_created(self):
        self.assertEqual(self.user.profile.user, self.user)

    def test_login_requires_valid_password(self):
        response = self.client.post(reverse("login"), {"username": "demo", "password": "incorrect"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_successful_login_and_role_redirect(self):
        response = self.client.post(reverse("login"), {"username": "demo", "password": "local-test-password"})
        self.assertRedirects(response, reverse("portal_home"), fetch_redirect_response=False)
        self.assertRedirects(self.client.get(reverse("portal_home")), reverse("dashboard_solicitante"), fetch_redirect_response=False)

    def test_anonymous_cannot_open_dashboard(self):
        self.assertEqual(self.client.get(reverse("dashboard_admin")).status_code, 302)

    def test_solicitante_cannot_open_admin_dashboard(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard_admin"))
        self.assertRedirects(response, reverse("portal_home"), fetch_redirect_response=False)


class DemoSeedTests(TestCase):
    @override_settings(DEBUG=False)
    def test_seed_rejected_outside_development(self):
        with self.assertRaises(CommandError):
            seed_demo_users()
        self.assertFalse(get_user_model().objects.exists())

    @override_settings(DEBUG=True)
    def test_existing_accounts_and_passwords_are_preserved(self):
        entry = next(iter(USER_DIRECTORY_MAP.values()))
        existing = get_user_model().objects.create_user(entry["sso"], password="personal-password", first_name="Preserved")
        personal_group = Group.objects.create(name="PERSONAL")
        existing.groups.add(personal_group)
        seed_demo_users()
        existing.refresh_from_db()
        self.assertTrue(existing.check_password("personal-password"))
        self.assertEqual(existing.first_name, "Preserved")
        self.assertFalse(existing.is_staff)
        self.assertQuerySetEqual(existing.groups.all(), [personal_group])
        self.assertEqual(seed_demo_users(), 0)


