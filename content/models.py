"""
Content app models.
Models for site content management: navbar, hero, about, vision, mission, value, team, 
announcements, activities, location, contact.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


class SiteSettings(models.Model):
    """Site-wide settings (singleton model)."""
    
    site_name = models.CharField(_('site name'), max_length=200, default='SaiReeCMPO')
    site_title = models.CharField(_('site title'), max_length=200, default='Government Office CMS')
    site_description = models.TextField(_('site description'), blank=True)
    logo = models.ImageField(_('logo'), upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(_('favicon'), upload_to='site/', blank=True, null=True)
    
    # Contact info
    phone = models.CharField(_('phone'), max_length=50, blank=True)
    email = models.EmailField(_('email'), blank=True)
    address = models.TextField(_('address'), blank=True)
    
    # Social media
    facebook_url = models.URLField(_('Facebook URL'), blank=True)
    twitter_url = models.URLField(_('Twitter URL'), blank=True)
    instagram_url = models.URLField(_('Instagram URL'), blank=True)
    youtube_url = models.URLField(_('YouTube URL'), blank=True)
    line_url = models.URLField(_('LINE URL'), blank=True)
    
    # Footer
    footer_text = models.TextField(_('footer text'), blank=True)
    copyright_text = models.CharField(_('copyright text'), max_length=200, blank=True)
    
    class Meta:
        verbose_name = _('site settings')
        verbose_name_plural = _('site settings')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create site settings singleton."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class NavbarMenu(models.Model):
    """Navbar menu items."""
    
    title = models.CharField(_('title'), max_length=100)
    url = models.CharField(_('URL'), max_length=200, help_text='Use # for anchor links')
    icon = models.CharField(_('icon class'), max_length=50, blank=True, help_text='Font Awesome class')
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='children',
        verbose_name=_('parent menu')
    )
    
    class Meta:
        ordering = ['order']
        verbose_name = _('navbar menu')
        verbose_name_plural = _('navbar menus')

    def __str__(self):
        return self.title


class HeroSlide(models.Model):
    """Hero section slides."""
    
    title = models.CharField(_('title'), max_length=200)
    subtitle = models.TextField(_('subtitle'), blank=True)
    button_text = models.CharField(_('button text'), max_length=50, blank=True)
    button_url = models.CharField(_('button URL'), max_length=200, blank=True)
    image = models.ImageField(_('background image'), upload_to='hero/')
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = _('hero slide')
        verbose_name_plural = _('hero slides')

    def __str__(self):
        return self.title


class AboutSection(models.Model):
    """About section content."""
    
    title = models.CharField(_('title'), max_length=200)
    content = CKEditor5Field(_('content'), config_name='extends')
    image = models.ImageField(_('image'), upload_to='about/', blank=True, null=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = _('about section')
        verbose_name_plural = _('about sections')

    def __str__(self):
        return self.title


class VisionMissionValue(models.Model):
    """Vision, Mission, and Values content."""
    
    TYPE_CHOICES = [
        ('vision', _('Vision')),
        ('mission', _('Mission')),
        ('value', _('Value')),
    ]
    
    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(_('title'), max_length=200)
    content = CKEditor5Field(_('content'), config_name='default')
    icon = models.CharField(_('icon class'), max_length=50, blank=True)
    image = models.ImageField(_('image'), upload_to='vmv/', blank=True, null=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        ordering = ['type', 'order']
        verbose_name = _('vision/mission/value')
        verbose_name_plural = _('vision/mission/values')

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"


class TeamMember(models.Model):
    """Team members."""
    
    name = models.CharField(_('name'), max_length=100)
    position = models.CharField(_('position'), max_length=100)
    bio = models.TextField(_('biography'), blank=True)
    image = models.ImageField(_('photo'), upload_to='team/')
    email = models.EmailField(_('email'), blank=True)
    phone = models.CharField(_('phone'), max_length=50, blank=True)
    
    # Social links
    facebook = models.URLField(_('Facebook'), blank=True)
    twitter = models.URLField(_('Twitter'), blank=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True)
    instagram = models.URLField(_('Instagram'), blank=True)
    
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = _('team member')
        verbose_name_plural = _('team members')

    def __str__(self):
        return self.name


class Announcement(models.Model):
    """Announcements/News."""
    
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('normal', _('Normal')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    
    title = models.CharField(_('title'), max_length=200)
    short_description = models.TextField(_('short description'), max_length=500)
    content = CKEditor5Field(_('content'), config_name='extends')
    image = models.ImageField(_('image'), upload_to='announcements/', blank=True, null=True)
    attachment = models.FileField(_('attachment'), upload_to='announcements/files/', blank=True, null=True)
    priority = models.CharField(_('priority'), max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    published_date = models.DateField(_('published date'), auto_now_add=True)
    expiry_date = models.DateField(_('expiry date'), null=True, blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    is_featured = models.BooleanField(_('is featured'), default=False)
    view_count = models.PositiveIntegerField(_('view count'), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-published_date']
        verbose_name = _('announcement')
        verbose_name_plural = _('announcements')

    def __str__(self):
        return self.title


class Activity(models.Model):
    """Activities/Events."""
    
    title = models.CharField(_('title'), max_length=200)
    short_description = models.TextField(_('short description'), max_length=500)
    content = CKEditor5Field(_('content'), config_name='extends')
    image = models.ImageField(_('featured image'), upload_to='activities/')
    
    event_date = models.DateField(_('event date'))
    event_time = models.TimeField(_('event time'), blank=True, null=True)
    location = models.CharField(_('location'), max_length=200, blank=True)
    
    is_active = models.BooleanField(_('is active'), default=True)
    is_featured = models.BooleanField(_('is featured'), default=False)
    view_count = models.PositiveIntegerField(_('view count'), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-event_date']
        verbose_name = _('activity')
        verbose_name_plural = _('activities')

    def __str__(self):
        return self.title


class ActivityGallery(models.Model):
    """Activity photo gallery."""
    
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(_('image'), upload_to='activities/gallery/')
    caption = models.CharField(_('caption'), max_length=200, blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = _('activity gallery image')
        verbose_name_plural = _('activity gallery images')

    def __str__(self):
        return f"Image for {self.activity.title}"


class Location(models.Model):
    """Office location."""
    
    name = models.CharField(_('location name'), max_length=200)
    address = models.TextField(_('address'))
    phone = models.CharField(_('phone'), max_length=50, blank=True)
    fax = models.CharField(_('fax'), max_length=50, blank=True)
    email = models.EmailField(_('email'), blank=True)
    
    # Map
    latitude = models.DecimalField(_('latitude'), max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(_('longitude'), max_digits=10, decimal_places=7, blank=True, null=True)
    google_maps_embed = models.TextField(_('Google Maps embed code'), blank=True)
    
    # Working hours
    working_hours = models.TextField(_('working hours'), blank=True)
    
    is_main = models.BooleanField(_('is main office'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    
    class Meta:
        ordering = ['-is_main', 'order']
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    """Contact form messages."""
    
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=50, blank=True)
    subject = models.CharField(_('subject'), max_length=200)
    message = models.TextField(_('message'))
    
    is_read = models.BooleanField(_('is read'), default=False)
    is_replied = models.BooleanField(_('is replied'), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('contact message')
        verbose_name_plural = _('contact messages')

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Feature(models.Model):
    """Feature/highlight boxes."""
    
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'))
    icon = models.CharField(_('icon class'), max_length=50, blank=True)
    number = models.CharField(_('display number'), max_length=10, blank=True)
    url = models.URLField(_('URL'), blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = _('feature')
        verbose_name_plural = _('features')

    def __str__(self):
        return self.title
