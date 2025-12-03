"""
Accounts app URL configuration.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # MFA
    path('mfa/verify/', views.MFAVerifyView.as_view(), name='mfa_verify'),
    path('mfa/setup/', views.MFASetupView.as_view(), name='mfa_setup'),
    path('mfa/disable/', views.MFADisableView.as_view(), name='mfa_disable'),
    
    # Password Reset
    path('password/reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password/reset/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Profile and Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
