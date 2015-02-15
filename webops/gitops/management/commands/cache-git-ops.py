from django.core.management.base import BaseCommand, CommandError
from gitops import helpers

class Command(BaseCommand):
    
    can_import_settings = True

    def handle(self, *args, **options):

        helpers.bootstrap()