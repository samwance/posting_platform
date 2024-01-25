from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            phone_number="12",
            is_superuser=True,
            is_staff=True,
            is_active=True,
            username="admin1",
            birth_date='2003-01-01'
        )

        user.set_password("123")
        user.save()
