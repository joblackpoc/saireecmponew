"""
Download app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'download'

urlpatterns = [
    # Public
    path('', views.DownloadListView.as_view(), name='list'),
    path('<int:pk>/', views.DownloadDetailView.as_view(), name='detail'),
    path('<int:pk>/download/', views.download_file, name='download'),
    path('<int:pk>/view-pdf/', views.view_pdf, name='view_pdf'),
    
    # Dashboard - Files
    path('dashboard/', views.DashboardDownloadListView.as_view(), name='dashboard_list'),
    path('dashboard/add/', views.DashboardDownloadCreateView.as_view(), name='dashboard_add'),
    path('dashboard/<int:pk>/edit/', views.DashboardDownloadUpdateView.as_view(), name='dashboard_edit'),
    path('dashboard/<int:pk>/delete/', views.DashboardDownloadDeleteView.as_view(), name='dashboard_delete'),
    
    # Dashboard - Categories
    path('dashboard/categories/', views.DashboardCategoryListView.as_view(), name='dashboard_category_list'),
    path('dashboard/categories/add/', views.DashboardCategoryCreateView.as_view(), name='dashboard_category_add'),
    path('dashboard/categories/<int:pk>/edit/', views.DashboardCategoryUpdateView.as_view(), name='dashboard_category_edit'),
    path('dashboard/categories/<int:pk>/delete/', views.DashboardCategoryDeleteView.as_view(), name='dashboard_category_delete'),
    
    # Dashboard - Logs
    path('dashboard/logs/', views.DashboardDownloadLogListView.as_view(), name='dashboard_log_list'),
]
