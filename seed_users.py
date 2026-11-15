"""Cria contas ficticias em desenvolvimento, preservando contas ja existentes."""

import os


def seed_demo_users():
    from django.conf import settings
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    from django.core.management.base import CommandError
    from django.db import transaction

    from accounts.directory import DEFAULT_PASSWORD_PLACEHOLDER, PROFILE_KEY_INFO, USER_DIRECTORY_MAP

    if not settings.DEBUG:
        raise CommandError("Seed de demonstracao permitido somente com DJANGO_DEBUG=1.")

    user_model = get_user_model()
    created = 0
    with transaction.atomic():
        groups = {
            name: Group.objects.get_or_create(name=name)[0]
            for name in ("ADMIN", "SOLICITANTE", "PROJETISTA", "DISPOSITIVOS")
        }
        for entry in USER_DIRECTORY_MAP.values():
            # Reexecutar nao redefine senhas, grupos, privilegios nem nomes existentes.
            if user_model.objects.filter(username=entry["sso"]).exists():
                continue
            first, _, last = entry["full_name"].strip().partition(" ")
            group_name = PROFILE_KEY_INFO.get(entry["profile_key"], {}).get("group") or "SOLICITANTE"
            user = user_model.objects.create_user(
                username=entry["sso"], password=DEFAULT_PASSWORD_PLACEHOLDER,
                first_name=first, last_name=last, email=entry.get("email", ""),
                is_staff=group_name == "ADMIN",
            )
            user.groups.add(groups[group_name])
            created += 1
    return created


if __name__ == "__main__":
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    print(f"Usuarios ficticios criados: {seed_demo_users()}. Contas existentes preservadas.")
