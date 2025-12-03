"""
Management command to initialize site settings.
"""

from django.core.management.base import BaseCommand
from content.models import SiteSettings


class Command(BaseCommand):
    help = 'Initialize site settings and basic data'

    def handle(self, *args, **options):
        """Create initial site settings."""
        
        self.stdout.write('Initializing site settings...')
        
        settings = SiteSettings.get_settings()
        
        self.stdout.write(self.style.SUCCESS(
            f'✓ Site settings initialized: {settings.site_name}'
        ))
        
        self.stdout.write(self.style.SUCCESS(
            '\nSite initialization complete!'
        ))
        self.stdout.write(
            'You can now customize the settings in the Django admin panel.'
        )
