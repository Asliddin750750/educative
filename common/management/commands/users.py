from django.core.management import BaseCommand

from account.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser(username='admin', password='1')
        User.objects.create_user(username='teacher1', password='1', job=1)
        User.objects.create_user(username='teacher2', password='1', job=1)
        User.objects.create_user(username='student1', password='1', job=2)
        User.objects.create_user(username='student2', password='1', job=2)
        User.objects.create_user(username='student3', password='1', job=2)
        User.objects.create_user(username='student4', password='1', job=2)
