"""
Accounts app views.
Login, Registration, MFA, Password Reset, and Dashboard views.
"""

import io
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import qrcode

from .models import LoginAttempt, PasswordResetToken
from .forms import (
    CustomLoginForm,
    MFAVerificationForm,
    MFASetupForm,
    UserRegistrationForm,
    PasswordResetRequestForm,
    CustomPasswordResetForm,
    CustomPasswordChangeForm,
    UserProfileForm
)

User = get_user_model()


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class LoginView(View):
    """Custom login view with MFA support."""
    
    template_name = 'accounts/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = CustomLoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomLoginForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            
            # Log successful authentication attempt
            LoginAttempt.objects.create(
                email=user.email,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                successful=True
            )
            
            # Check if MFA is enabled
            if user.mfa_enabled:
                # Store user ID in session for MFA verification
                request.session['mfa_user_id'] = user.id
                request.session['mfa_remember_me'] = form.cleaned_data.get('remember_me', False)
                return redirect('accounts:mfa_verify')
            
            # No MFA, proceed with login
            login(request, user)
            
            # Handle remember me
            if not form.cleaned_data.get('remember_me', False):
                request.session.set_expiry(0)
            
            messages.success(request, f'Welcome back, {user.first_name}!')
            
            # Redirect to next URL or dashboard
            next_url = request.GET.get('next', reverse('accounts:dashboard'))
            return redirect(next_url)
        else:
            # Log failed login attempt
            email = request.POST.get('username', '')
            LoginAttempt.objects.create(
                email=email,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                successful=False
            )
            messages.error(request, 'Invalid email or password.')
        
        return render(request, self.template_name, {'form': form})


class MFAVerifyView(View):
    """MFA verification view."""
    
    template_name = 'accounts/mfa_verify.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if MFA user ID is in session
        if 'mfa_user_id' not in request.session:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = MFAVerificationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = MFAVerificationForm(request.POST)
        
        if form.is_valid():
            user_id = request.session.get('mfa_user_id')
            user = get_object_or_404(User, id=user_id)
            token = form.cleaned_data['token']
            use_backup = form.cleaned_data.get('use_backup_code', False)
            
            # Verify token
            if use_backup:
                valid = user.verify_backup_code(token)
                if valid:
                    messages.info(request, 'Backup code used. You have '
                                 f'{user.get_remaining_backup_codes_count()} codes remaining.')
            else:
                valid = user.verify_mfa_token(token)
            
            if valid:
                # Clear MFA session data
                del request.session['mfa_user_id']
                remember_me = request.session.pop('mfa_remember_me', False)
                
                # Complete login
                login(request, user)
                
                if not remember_me:
                    request.session.set_expiry(0)
                
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        
        return render(request, self.template_name, {'form': form})


class MFASetupView(LoginRequiredMixin, View):
    """MFA setup view."""
    
    template_name = 'accounts/mfa_setup.html'
    
    def get(self, request):
        user = request.user
        
        # Generate new secret if not exists
        if not user.mfa_secret:
            user.generate_mfa_secret()
            user.save()
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(user.get_mfa_uri())
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        form = MFASetupForm()
        context = {
            'form': form,
            'qr_code': qr_code_base64,
            'secret': user.mfa_secret,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = MFASetupForm(request.POST)
        user = request.user
        
        if form.is_valid():
            token = form.cleaned_data['token']
            
            if user.verify_mfa_token(token):
                # Enable MFA
                user.mfa_enabled = True
                backup_codes = user.generate_backup_codes()
                user.save()
                
                messages.success(request, 'MFA has been enabled successfully!')
                
                # Show backup codes
                return render(request, 'accounts/mfa_backup_codes.html', {
                    'backup_codes': backup_codes
                })
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        
        # Re-generate QR code for display
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(user.get_mfa_uri())
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        context = {
            'form': form,
            'qr_code': qr_code_base64,
            'secret': user.mfa_secret,
        }
        return render(request, self.template_name, context)


class MFADisableView(LoginRequiredMixin, View):
    """Disable MFA view."""
    
    def post(self, request):
        user = request.user
        user.mfa_enabled = False
        user.mfa_secret = ''
        user.mfa_backup_codes = ''
        user.save()
        
        messages.success(request, 'MFA has been disabled.')
        return redirect('accounts:profile')


class LogoutView(View):
    """Logout view."""
    
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('content:landing')
    
    def post(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('content:landing')


class RegisterView(View):
    """User registration view."""
    
    template_name = 'accounts/register.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the system.')
            return redirect('accounts:dashboard')
        
        return render(request, self.template_name, {'form': form})


class PasswordResetRequestView(View):
    """Password reset request view."""
    
    template_name = 'accounts/password_reset.html'
    
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                # Create reset token
                token = PasswordResetToken.generate_token()
                PasswordResetToken.objects.create(user=user, token=token)
                
                # Build reset URL
                reset_url = request.build_absolute_uri(
                    reverse('accounts:password_reset_confirm', kwargs={'token': token})
                )
                
                # Send email (console backend in development)
                subject = 'Password Reset Request'
                message = f'''
Hello {user.first_name},

You have requested to reset your password. Click the link below to reset:

{reset_url}

This link will expire in 24 hours.

If you did not request this reset, please ignore this email.

Best regards,
SaiReeCMPO Team
                '''
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@saireecmpo.com',
                    [email],
                    fail_silently=True,
                )
                
                messages.success(request, 
                    'If an account exists with that email, you will receive a password reset link.')
                
            except User.DoesNotExist:
                # Don't reveal that user doesn't exist
                messages.success(request, 
                    'If an account exists with that email, you will receive a password reset link.')
        
        return render(request, self.template_name, {'form': form})


class PasswordResetConfirmView(View):
    """Password reset confirmation view."""
    
    template_name = 'accounts/password_reset_confirm.html'
    
    def dispatch(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            self.reset_token = PasswordResetToken.objects.get(token=token)
            if not self.reset_token.is_valid():
                messages.error(request, 'This password reset link has expired or been used.')
                return redirect('accounts:password_reset')
        except PasswordResetToken.DoesNotExist:
            messages.error(request, 'Invalid password reset link.')
            return redirect('accounts:password_reset')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, token):
        form = CustomPasswordResetForm(user=self.reset_token.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, token):
        form = CustomPasswordResetForm(user=self.reset_token.user, data=request.POST)
        
        if form.is_valid():
            form.save()
            
            # Mark token as used
            self.reset_token.used = True
            self.reset_token.save()
            
            # Update password changed timestamp
            user = self.reset_token.user
            user.password_changed_at = timezone.now()
            user.save()
            
            messages.success(request, 'Your password has been reset successfully. You can now login.')
            return redirect('accounts:login')
        
        return render(request, self.template_name, {'form': form})


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view."""
    
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Import models here to avoid circular imports
        from blog.models import BlogPost
        from download.models import DownloadFile
        from pdfapp.models import PDFDocument
        from content.models import Announcement, Activity
        
        context['recent_posts'] = BlogPost.objects.filter(is_published=True)[:5]
        context['recent_downloads'] = DownloadFile.objects.filter(is_active=True)[:5]
        context['recent_pdfs'] = PDFDocument.objects.filter(user=self.request.user)[:5]
        context['announcements'] = Announcement.objects.filter(is_active=True)[:5]
        context['activities'] = Activity.objects.filter(is_active=True)[:5]
        
        # Stats
        context['total_posts'] = BlogPost.objects.count()
        context['total_downloads'] = DownloadFile.objects.count()
        context['total_pdfs'] = PDFDocument.objects.filter(user=self.request.user).count()
        context['module'] = 'dashboard'
        
        return context


class ProfileView(LoginRequiredMixin, View):
    """User profile view."""
    
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
        return render(request, self.template_name, {
            'form': form,
            'password_form': password_form
        })
    
    def post(self, request):
        if 'update_profile' in request.POST:
            form = UserProfileForm(request.POST, request.FILES, instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
        
        elif 'change_password' in request.POST:
            form = UserProfileForm(instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            
            if password_form.is_valid():
                password_form.save()
                # Update session to prevent logout
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully!')
                return redirect('accounts:profile')
        
        else:
            form = UserProfileForm(instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user)
        
        return render(request, self.template_name, {
            'form': form,
            'password_form': password_form
        })
