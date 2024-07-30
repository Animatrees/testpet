import os
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Save the current state of the database to a fixture.'

    def add_arguments(self, parser):
        parser.add_argument('fixture_name', type=str, help='The name of the fixture file to save.')

    def handle(self, *args, **kwargs):
        fixture_name = kwargs['fixture_name']
        fixture_path = os.path.join('fixtures', f'{fixture_name}.json')
        os.makedirs(os.path.dirname(fixture_path), exist_ok=True)
        call_command('dumpdata', '--output', fixture_path)
        self.stdout.write(self.style.SUCCESS(f'Database saved to {fixture_path}'))
