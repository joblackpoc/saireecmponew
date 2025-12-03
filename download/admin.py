"""
Download app admin configuration.
"""

from django.contrib import admin
from .models import DownloadFile, DownloadCategory, DownloadLog


@admin.register(DownloadCategory)
class DownloadCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')


@admin.register(DownloadFile)
class DownloadFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'file_extension', 'file_size', 'uploaded_by', 
                    'is_active', 'is_featured', 'download_count', 'created_at')
    list_filter = ('is_active', 'is_featured', 'category', 'created_at')
    list_editable = ('is_active', 'is_featured')
    search_fields = ('title', 'short_description')
    date_hierarchy = 'created_at'
    readonly_fields = ('download_count', 'created_at', 'updated_at')


@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'ip_address', 'downloaded_at')
    list_filter = ('downloaded_at', 'file')
    search_fields = ('file__title', 'ip_address')
    date_hierarchy = 'downloaded_at'
    readonly_fields = ('file', 'user', 'ip_address', 'user_agent', 'downloaded_at')
