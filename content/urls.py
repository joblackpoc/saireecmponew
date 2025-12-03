"""
Content app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Public pages
    path('', views.landing_page, name='landing'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('activity/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('activities/', views.activities_list, name='activities_list'),
    
    # Dashboard - Site Settings
    path('dashboard/settings/', views.dashboard_site_settings, name='dashboard_site_settings'),
    
    # Dashboard - Navbar
    path('dashboard/navbar/', views.NavbarMenuListView.as_view(), name='dashboard_navbar_list'),
    path('dashboard/navbar/add/', views.NavbarMenuCreateView.as_view(), name='dashboard_navbar_add'),
    path('dashboard/navbar/<int:pk>/edit/', views.NavbarMenuUpdateView.as_view(), name='dashboard_navbar_edit'),
    path('dashboard/navbar/<int:pk>/delete/', views.NavbarMenuDeleteView.as_view(), name='dashboard_navbar_delete'),
    
    # Dashboard - Hero
    path('dashboard/hero/', views.HeroSlideListView.as_view(), name='dashboard_hero_list'),
    path('dashboard/hero/add/', views.HeroSlideCreateView.as_view(), name='dashboard_hero_add'),
    path('dashboard/hero/<int:pk>/edit/', views.HeroSlideUpdateView.as_view(), name='dashboard_hero_edit'),
    path('dashboard/hero/<int:pk>/delete/', views.HeroSlideDeleteView.as_view(), name='dashboard_hero_delete'),
    
    # Dashboard - About
    path('dashboard/about/', views.AboutSectionListView.as_view(), name='dashboard_about_list'),
    path('dashboard/about/add/', views.AboutSectionCreateView.as_view(), name='dashboard_about_add'),
    path('dashboard/about/<int:pk>/edit/', views.AboutSectionUpdateView.as_view(), name='dashboard_about_edit'),
    path('dashboard/about/<int:pk>/delete/', views.AboutSectionDeleteView.as_view(), name='dashboard_about_delete'),
    
    # Dashboard - Vision/Mission/Values
    path('dashboard/vmv/', views.VMVListView.as_view(), name='dashboard_vmv_list'),
    path('dashboard/vmv/add/', views.VMVCreateView.as_view(), name='dashboard_vmv_add'),
    path('dashboard/vmv/<int:pk>/edit/', views.VMVUpdateView.as_view(), name='dashboard_vmv_edit'),
    path('dashboard/vmv/<int:pk>/delete/', views.VMVDeleteView.as_view(), name='dashboard_vmv_delete'),
    
    # Dashboard - Team
    path('dashboard/team/', views.TeamMemberListView.as_view(), name='dashboard_team_list'),
    path('dashboard/team/add/', views.TeamMemberCreateView.as_view(), name='dashboard_team_add'),
    path('dashboard/team/<int:pk>/edit/', views.TeamMemberUpdateView.as_view(), name='dashboard_team_edit'),
    path('dashboard/team/<int:pk>/delete/', views.TeamMemberDeleteView.as_view(), name='dashboard_team_delete'),
    
    # Dashboard - Announcements
    path('dashboard/announcements/', views.AnnouncementListView.as_view(), name='dashboard_announcement_list'),
    path('dashboard/announcements/add/', views.AnnouncementCreateView.as_view(), name='dashboard_announcement_add'),
    path('dashboard/announcements/<int:pk>/edit/', views.AnnouncementUpdateView.as_view(), name='dashboard_announcement_edit'),
    path('dashboard/announcements/<int:pk>/delete/', views.AnnouncementDeleteView.as_view(), name='dashboard_announcement_delete'),
    
    # Dashboard - Activities
    path('dashboard/activities/', views.ActivityListView.as_view(), name='dashboard_activity_list'),
    path('dashboard/activities/add/', views.ActivityCreateView.as_view(), name='dashboard_activity_add'),
    path('dashboard/activities/<int:pk>/edit/', views.ActivityUpdateView.as_view(), name='dashboard_activity_edit'),
    path('dashboard/activities/<int:pk>/delete/', views.ActivityDeleteView.as_view(), name='dashboard_activity_delete'),
    
    # Dashboard - Locations
    path('dashboard/locations/', views.LocationListView.as_view(), name='dashboard_location_list'),
    path('dashboard/locations/add/', views.LocationCreateView.as_view(), name='dashboard_location_add'),
    path('dashboard/locations/<int:pk>/edit/', views.LocationUpdateView.as_view(), name='dashboard_location_edit'),
    path('dashboard/locations/<int:pk>/delete/', views.LocationDeleteView.as_view(), name='dashboard_location_delete'),
    
    # Dashboard - Contact Messages
    path('dashboard/contacts/', views.ContactMessageListView.as_view(), name='dashboard_contact_list'),
    path('dashboard/contacts/<int:pk>/', views.ContactMessageDetailView.as_view(), name='dashboard_contact_detail'),
    path('dashboard/contacts/<int:pk>/delete/', views.ContactMessageDeleteView.as_view(), name='dashboard_contact_delete'),
    
    # Dashboard - Features
    path('dashboard/features/', views.FeatureListView.as_view(), name='dashboard_feature_list'),
    path('dashboard/features/add/', views.FeatureCreateView.as_view(), name='dashboard_feature_add'),
    path('dashboard/features/<int:pk>/edit/', views.FeatureUpdateView.as_view(), name='dashboard_feature_edit'),
    path('dashboard/features/<int:pk>/delete/', views.FeatureDeleteView.as_view(), name='dashboard_feature_delete'),
]
