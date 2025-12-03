"""
Accounts app admin configuration.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, LoginAttempt, PasswordResetToken


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom User admin."""
    
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'mfa_enabled')
    list_filter = ('is_staff', 'is_active', 'mfa_enabled', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'avatar', 'position', 'department')}),
        (_('MFA'), {'fields': ('mfa_enabled', 'mfa_secret')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'password_changed_at')}),
        (_('Security'), {'fields': ('failed_login_attempts', 'last_failed_login')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'password_changed_at')


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """Login attempt admin."""
    
    list_display = ('email', 'ip_address', 'successful', 'timestamp')
    list_filter = ('successful', 'timestamp')
    search_fields = ('email', 'ip_address')
    readonly_fields = ('email', 'ip_address', 'user_agent', 'successful', 'timestamp')
    ordering = ('-timestamp',)


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Password reset token admin."""
    
    list_display = ('user', 'created_at', 'used')
    list_filter = ('used', 'created_at')
    search_fields = ('user__email',)
    readonly_fields = ('token', 'created_at')
