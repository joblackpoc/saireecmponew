"""
PDF app admin configuration.
"""

from django.contrib import admin
from .models import PDFDocument, ConversionLog


class ConversionLogInline(admin.TabularInline):
    model = ConversionLog
    extra = 0
    readonly_fields = ('action', 'message', 'timestamp')
    can_delete = False


@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'source_extension', 'status', 'has_pdf', 'has_html', 
                    'view_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'user__email')
    date_hierarchy = 'created_at'
    readonly_fields = ('status', 'error_message', 'page_count', 'view_count', 
                       'created_at', 'updated_at', 'processed_at')
    inlines = [ConversionLogInline]


@admin.register(ConversionLog)
class ConversionLogAdmin(admin.ModelAdmin):
    list_display = ('document', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('document__title', 'message')
    date_hierarchy = 'timestamp'
    readonly_fields = ('document', 'action', 'message', 'timestamp')
