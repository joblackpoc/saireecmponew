"""
Download app models.
File downloads with support for PDF, DOCX, XLSX, PPTX, ZIP, RAR.
"""

import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


def upload_to_downloads(instance, filename):
    """Custom upload path for download files."""
    ext = filename.split('.')[-1].lower()
    return f'downloads/{ext}/{filename}'


class DownloadCategory(models.Model):
    """Download category."""
    
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icon class'), max_length=50, blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = _('download category')
        verbose_name_plural = _('download categories')

    def __str__(self):
        return self.name


class DownloadFile(models.Model):
    """Downloadable file model."""
    
    ALLOWED_EXTENSIONS = ['pdf', 'docx', 'xlsx', 'pptx', 'zip', 'rar']
    
    title = models.CharField(_('title'), max_length=200)
    short_description = models.TextField(_('short description'), max_length=500)
    description = models.TextField(_('full description'), blank=True)
    file = models.FileField(
        _('file'),
        upload_to=upload_to_downloads,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)]
    )
    
    category = models.ForeignKey(
        DownloadCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='files',
        verbose_name=_('category')
    )
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_files',
        verbose_name=_('uploaded by')
    )
    
    download_count = models.PositiveIntegerField(_('download count'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    is_featured = models.BooleanField(_('is featured'), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('download file')
        verbose_name_plural = _('download files')

    def __str__(self):
        return self.title

    @property
    def file_extension(self):
        """Get file extension."""
        if self.file:
            return os.path.splitext(self.file.name)[1][1:].lower()
        return ''

    @property
    def file_size(self):
        """Get file size in human-readable format."""
        if self.file:
            size = self.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        return '0 B'

    @property
    def is_pdf(self):
        """Check if file is PDF."""
        return self.file_extension == 'pdf'

    @property
    def file_icon(self):
        """Get appropriate icon class for file type."""
        icons = {
            'pdf': 'fa-file-pdf-o',
            'docx': 'fa-file-word-o',
            'xlsx': 'fa-file-excel-o',
            'pptx': 'fa-file-powerpoint-o',
            'zip': 'fa-file-archive-o',
            'rar': 'fa-file-archive-o',
        }
        return icons.get(self.file_extension, 'fa-file-o')


class DownloadLog(models.Model):
    """Track file downloads."""
    
    file = models.ForeignKey(DownloadFile, on_delete=models.CASCADE, related_name='download_logs')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='download_logs'
    )
    ip_address = models.GenericIPAddressField(_('IP address'))
    user_agent = models.TextField(_('user agent'), blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-downloaded_at']
        verbose_name = _('download log')
        verbose_name_plural = _('download logs')

    def __str__(self):
        return f"{self.file.title} - {self.downloaded_at}"
