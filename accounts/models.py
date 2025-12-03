"""
Accounts app models.
Custom User model with MFA (Google Authenticator) support.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import pyotp
import secrets


class CustomUserManager(BaseUserManager):
    """Custom user manager for CustomUser model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom User model with email as username and MFA support."""
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    position = models.CharField(_('position'), max_length=100, blank=True)
    department = models.CharField(_('department'), max_length=100, blank=True)
    
    # MFA Fields
    mfa_enabled = models.BooleanField(_('MFA enabled'), default=False)
    mfa_secret = models.CharField(_('MFA secret'), max_length=32, blank=True)
    mfa_backup_codes = models.TextField(_('MFA backup codes'), blank=True)
    
    # Security fields
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    password_changed_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def generate_mfa_secret(self):
        """Generate a new MFA secret for Google Authenticator."""
        self.mfa_secret = pyotp.random_base32()
        return self.mfa_secret

    def get_mfa_uri(self):
        """Get the MFA URI for QR code generation."""
        if not self.mfa_secret:
            self.generate_mfa_secret()
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.provisioning_uri(name=self.email, issuer_name="SaiReeCMPO")

    def verify_mfa_token(self, token):
        """Verify the MFA token."""
        if not self.mfa_secret:
            return False
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.verify(token, valid_window=1)

    def generate_backup_codes(self, count=10):
        """Generate backup codes for MFA recovery."""
        codes = [secrets.token_hex(4).upper() for _ in range(count)]
        self.mfa_backup_codes = ','.join(codes)
        return codes

    def verify_backup_code(self, code):
        """Verify and consume a backup code."""
        if not self.mfa_backup_codes:
            return False
        codes = self.mfa_backup_codes.split(',')
        if code.upper() in codes:
            codes.remove(code.upper())
            self.mfa_backup_codes = ','.join(codes)
            self.save()
            return True
        return False

    def get_remaining_backup_codes_count(self):
        """Get the count of remaining backup codes."""
        if not self.mfa_backup_codes:
            return 0
        return len(self.mfa_backup_codes.split(','))


class LoginAttempt(models.Model):
    """Track login attempts for security."""
    
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    successful = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('login attempt')
        verbose_name_plural = _('login attempts')

    def __str__(self):
        status = "Success" if self.successful else "Failed"
        return f"{self.email} - {status} - {self.timestamp}"


class PasswordResetToken(models.Model):
    """Custom password reset token model."""
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reset token for {self.user.email}"

    @classmethod
    def generate_token(cls):
        """Generate a secure random token."""
        return secrets.token_urlsafe(48)

    def is_valid(self):
        """Check if token is still valid (not used and not expired - 24h)."""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.used:
            return False
        expiry_time = self.created_at + timedelta(hours=24)
        return timezone.now() < expiry_time
