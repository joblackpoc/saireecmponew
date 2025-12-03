"""
PDF app models.
Convert DOCX and PPTX to PDF and HTML with style preservation.
"""

import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


def upload_to_pdf_source(instance, filename):
    """Custom upload path for source files."""
    return f'pdf/source/{filename}'


def upload_to_pdf_output(instance, filename):
    """Custom upload path for output files."""
    return f'pdf/output/{filename}'


class PDFDocument(models.Model):
    """Document for PDF conversion."""
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]
    
    ALLOWED_EXTENSIONS = ['docx', 'pptx']
    
    title = models.CharField(_('title'), max_length=200)
    source_file = models.FileField(
        _('source file'),
        upload_to=upload_to_pdf_source,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)],
        help_text=_('Upload DOCX or PPTX file')
    )
    
    # Generated files
    pdf_file = models.FileField(
        _('PDF file'),
        upload_to=upload_to_pdf_output,
        blank=True,
        null=True
    )
    html_file = models.FileField(
        _('HTML file'),
        upload_to=upload_to_pdf_output,
        blank=True,
        null=True
    )
    html_content = models.TextField(_('HTML content'), blank=True)
    
    # Metadata
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pdf_documents',
        verbose_name=_('user')
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    error_message = models.TextField(_('error message'), blank=True)
    
    # Stats
    page_count = models.PositiveIntegerField(_('page count'), default=0)
    view_count = models.PositiveIntegerField(_('view count'), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(_('processed at'), null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('PDF document')
        verbose_name_plural = _('PDF documents')

    def __str__(self):
        return self.title

    @property
    def source_extension(self):
        """Get source file extension."""
        if self.source_file:
            return os.path.splitext(self.source_file.name)[1][1:].lower()
        return ''

    @property
    def source_size(self):
        """Get source file size."""
        if self.source_file:
            size = self.source_file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        return '0 B'

    @property
    def is_docx(self):
        return self.source_extension == 'docx'

    @property
    def is_pptx(self):
        return self.source_extension == 'pptx'

    @property
    def has_pdf(self):
        return bool(self.pdf_file)

    @property
    def has_html(self):
        return bool(self.html_file) or bool(self.html_content)


class ConversionLog(models.Model):
    """Track conversion history."""
    
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(_('action'), max_length=50)
    message = models.TextField(_('message'))
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('conversion log')
        verbose_name_plural = _('conversion logs')

    def __str__(self):
        return f"{self.document.title} - {self.action}"
