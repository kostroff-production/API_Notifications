from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notifications.settings import ADMIN


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            User.objects.create_superuser(username=ADMIN['login'], email=ADMIN['email'], password=ADMIN['password'])
        else:
            print('Admin accounts can only be initialized if no User exist')
