import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create CivicFix admin user"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME", "civicfixadmin")
        email = os.environ.get("ADMIN_EMAIL", "civicfixadmin@gmail.com")
        password = os.environ.get("ADMIN_PASSWORD")

        if not password:
            self.stdout.write(
                self.style.ERROR("ADMIN_PASSWORD environment variable is not set")
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING("Admin user already exists")
            )
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS("Admin user created successfully")
            )