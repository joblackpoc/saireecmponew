"""
PDF app forms.
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field

from .models import PDFDocument


class PDFDocumentForm(forms.ModelForm):
    """PDF document upload form."""
    
    class Meta:
        model = PDFDocument
        fields = ['title', 'source_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'source_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Upload & Convert', css_class='btn btn-primary'))
        
        self.fields['source_file'].help_text = 'Allowed formats: DOCX, PPTX'
