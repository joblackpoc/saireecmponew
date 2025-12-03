"""
PDF app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'pdfapp'

urlpatterns = [
    path('', views.PDFDocumentListView.as_view(), name='list'),
    path('upload/', views.PDFDocumentCreateView.as_view(), name='upload'),
    path('<int:pk>/', views.PDFDocumentDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.PDFDocumentDeleteView.as_view(), name='delete'),
    path('<int:pk>/view-pdf/', views.view_pdf, name='view_pdf'),
    path('<int:pk>/view-html/', views.view_html, name='view_html'),
    path('<int:pk>/export-html/', views.export_html, name='export_html'),
    path('<int:pk>/reprocess/', views.reprocess_document, name='reprocess'),
]
