"""
Blog app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Public
    path('', views.BlogListView.as_view(), name='list'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    path('<int:pk>/comment/', views.blog_comment_submit, name='comment_submit'),
    
    # Dashboard - Posts
    path('dashboard/', views.DashboardBlogListView.as_view(), name='dashboard_list'),
    path('dashboard/add/', views.DashboardBlogCreateView.as_view(), name='dashboard_add'),
    path('dashboard/<int:pk>/edit/', views.DashboardBlogUpdateView.as_view(), name='dashboard_edit'),
    path('dashboard/<int:pk>/delete/', views.DashboardBlogDeleteView.as_view(), name='dashboard_delete'),
    
    # Dashboard - Categories
    path('dashboard/categories/', views.DashboardCategoryListView.as_view(), name='dashboard_category_list'),
    path('dashboard/categories/add/', views.DashboardCategoryCreateView.as_view(), name='dashboard_category_add'),
    path('dashboard/categories/<int:pk>/edit/', views.DashboardCategoryUpdateView.as_view(), name='dashboard_category_edit'),
    path('dashboard/categories/<int:pk>/delete/', views.DashboardCategoryDeleteView.as_view(), name='dashboard_category_delete'),
    
    # Dashboard - Tags
    path('dashboard/tags/', views.DashboardTagListView.as_view(), name='dashboard_tag_list'),
    path('dashboard/tags/add/', views.DashboardTagCreateView.as_view(), name='dashboard_tag_add'),
    path('dashboard/tags/<int:pk>/edit/', views.DashboardTagUpdateView.as_view(), name='dashboard_tag_edit'),
    path('dashboard/tags/<int:pk>/delete/', views.DashboardTagDeleteView.as_view(), name='dashboard_tag_delete'),
    
    # Dashboard - Comments
    path('dashboard/comments/', views.DashboardCommentListView.as_view(), name='dashboard_comment_list'),
    path('dashboard/comments/<int:pk>/approve/', views.dashboard_comment_approve, name='dashboard_comment_approve'),
    path('dashboard/comments/<int:pk>/delete/', views.DashboardCommentDeleteView.as_view(), name='dashboard_comment_delete'),
]
