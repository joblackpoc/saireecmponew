"""
Content app admin configuration.
"""

from django.contrib import admin
from .models import (
    SiteSettings, NavbarMenu, HeroSlide, AboutSection, VisionMissionValue,
    TeamMember, Announcement, Activity, ActivityGallery, Location, 
    ContactMessage, Feature
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_title', 'email', 'phone')
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NavbarMenu)
class NavbarMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'is_active', 'parent')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title',)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')


@admin.register(VisionMissionValue)
class VisionMissionValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'order', 'is_active')
    list_filter = ('type', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'position')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'published_date', 'is_active', 'is_featured', 'view_count')
    list_filter = ('priority', 'is_active', 'is_featured', 'published_date')
    list_editable = ('is_active', 'is_featured')
    search_fields = ('title', 'short_description')
    date_hierarchy = 'published_date'


class ActivityGalleryInline(admin.TabularInline):
    model = ActivityGallery
    extra = 1


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'is_active', 'is_featured', 'view_count')
    list_filter = ('is_active', 'is_featured', 'event_date')
    list_editable = ('is_active', 'is_featured')
    search_fields = ('title', 'short_description')
    date_hierarchy = 'event_date'
    inlines = [ActivityGalleryInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_main', 'is_active', 'order')
    list_filter = ('is_main', 'is_active')
    list_editable = ('is_main', 'is_active', 'order')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'is_replied', 'created_at')
    list_filter = ('is_read', 'is_replied', 'created_at')
    list_editable = ('is_read', 'is_replied')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
