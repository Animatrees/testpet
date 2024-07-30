import os
from django.core.management import call_command
from django.test.runner import DiscoverRunner


class FixtureDiscoverRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        fixture_name = 'testdata'
        fixture_path = os.path.join('fixtures', f'{fixture_name}.json')
        if not os.path.exists(fixture_path):
            call_command('save_fixture', fixture_name)
        call_command('loaddata', fixture_path)  # Загрузите фикстуру с полным путем

    def teardown_test_environment(self, **kwargs):
        super().teardown_test_environment(**kwargs)
        fixture_name = 'testdata'
        fixture_path = os.path.join('fixtures', f'{fixture_name}.json')
        if os.path.exists(fixture_path):
            os.remove(fixture_path)
