"""
Content app context processors.
"""

from .models import SiteSettings, NavbarMenu
import logging

logger = logging.getLogger(__name__)


def site_settings(request):
    """Add site settings to template context."""
    
    try:
        settings = SiteSettings.get_settings()
    except Exception as e:
        logger.warning(f"Failed to load site settings: {e}")
        settings = None
    
    try:
        navbar_menus = NavbarMenu.objects.filter(is_active=True, parent__isnull=True)
    except Exception as e:
        logger.warning(f"Failed to load navbar menus: {e}")
        navbar_menus = []
    
    return {
        'site_settings': settings,
        'navbar_menus': navbar_menus,
    }
