"""
Download app views.
Public download pages and dashboard management.
"""

import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import FileResponse, Http404, HttpResponse
from django.db.models import Q
from django.conf import settings

from .models import DownloadFile, DownloadCategory, DownloadLog
from .forms import DownloadFileForm, DownloadCategoryForm


def get_client_ip(request):
    """Get client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Public Views
class DownloadListView(ListView):
    """Public download listing."""
    
    model = DownloadFile
    template_name = 'download/download_list.html'
    context_object_name = 'files'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = DownloadFile.objects.filter(is_active=True)
        
        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(short_description__icontains=query)
            )
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
        
        # File type filter
        file_type = self.request.GET.get('type')
        if file_type:
            queryset = queryset.filter(file__iendswith=f'.{file_type}')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DownloadCategory.objects.filter(is_active=True)
        context['featured_files'] = DownloadFile.objects.filter(is_active=True, is_featured=True)[:5]
        return context


class DownloadDetailView(DetailView):
    """Download detail view with PDF preview."""
    
    model = DownloadFile
    template_name = 'download/download_detail.html'
    context_object_name = 'file'
    
    def get_queryset(self):
        return DownloadFile.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_files'] = DownloadFile.objects.filter(
            is_active=True,
            category=self.object.category
        ).exclude(pk=self.object.pk)[:4]
        return context


def download_file(request, pk):
    """Handle file download."""
    
    file_obj = get_object_or_404(DownloadFile, pk=pk, is_active=True)
    
    # Log download
    DownloadLog.objects.create(
        file=file_obj,
        user=request.user if request.user.is_authenticated else None,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Increment download count
    file_obj.download_count += 1
    file_obj.save()
    
    # Serve file
    try:
        response = FileResponse(
            file_obj.file.open('rb'),
            as_attachment=True,
            filename=os.path.basename(file_obj.file.name)
        )
        return response
    except Exception as e:
        raise Http404("File not found")


def view_pdf(request, pk):
    """View PDF in browser."""
    
    file_obj = get_object_or_404(DownloadFile, pk=pk, is_active=True)
    
    if not file_obj.is_pdf:
        raise Http404("This file is not a PDF")
    
    try:
        response = FileResponse(
            file_obj.file.open('rb'),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_obj.file.name)}"'
        return response
    except Exception as e:
        raise Http404("File not found")


# Dashboard Views
class DashboardDownloadListView(LoginRequiredMixin, ListView):
    """Dashboard download listing."""
    
    model = DownloadFile
    template_name = 'dashboard/download_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'downloads'
        return context


class DashboardDownloadCreateView(LoginRequiredMixin, CreateView):
    """Dashboard download create."""
    
    model = DownloadFile
    form_class = DownloadFileForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('download:dashboard_list')
    
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'File uploaded successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'downloads'
        context['title'] = 'Upload File'
        return context


class DashboardDownloadUpdateView(LoginRequiredMixin, UpdateView):
    """Dashboard download update."""
    
    model = DownloadFile
    form_class = DownloadFileForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('download:dashboard_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'File updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'downloads'
        context['title'] = 'Edit File'
        return context


class DashboardDownloadDeleteView(LoginRequiredMixin, DeleteView):
    """Dashboard download delete."""
    
    model = DownloadFile
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('download:dashboard_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'File deleted successfully!')
        return super().form_valid(form)


# Category Dashboard Views
class DashboardCategoryListView(LoginRequiredMixin, ListView):
    model = DownloadCategory
    template_name = 'dashboard/download_category_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'download_categories'
        return context


class DashboardCategoryCreateView(LoginRequiredMixin, CreateView):
    model = DownloadCategory
    form_class = DownloadCategoryForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('download:dashboard_category_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'download_categories'
        context['title'] = 'Add Category'
        return context


class DashboardCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = DownloadCategory
    form_class = DownloadCategoryForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('download:dashboard_category_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'download_categories'
        context['title'] = 'Edit Category'
        return context


class DashboardCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = DownloadCategory
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('download:dashboard_category_list')


# Download Logs Dashboard
class DashboardDownloadLogListView(LoginRequiredMixin, ListView):
    model = DownloadLog
    template_name = 'dashboard/download_log_list.html'
    context_object_name = 'items'
    paginate_by = 50
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'download_logs'
        return context
