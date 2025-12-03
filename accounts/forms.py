"""
Accounts app forms.
Login, Registration, MFA, and Password Reset forms.
"""

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm
)
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, HTML, Row, Column

User = get_user_model()


class CustomLoginForm(AuthenticationForm):
    """Custom login form with crispy forms styling."""
    
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='mb-3'),
            Field('password', css_class='mb-3'),
            Div(
                Field('remember_me', wrapper_class='form-check'),
                css_class='mb-3'
            ),
            Submit('submit', 'Login', css_class='btn btn-primary w-100 mb-3')
        )


class MFAVerificationForm(forms.Form):
    """MFA token verification form."""
    
    token = forms.CharField(
        max_length=6,
        min_length=6,
        label='Authentication Code',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': '000000',
            'autocomplete': 'off',
            'inputmode': 'numeric',
            'pattern': '[0-9]*'
        })
    )
    use_backup_code = forms.BooleanField(
        required=False,
        label='Use backup code instead',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('token', css_class='mb-3'),
            Div(
                Field('use_backup_code', wrapper_class='form-check'),
                css_class='mb-3'
            ),
            Submit('submit', 'Verify', css_class='btn btn-primary w-100')
        )


class MFASetupForm(forms.Form):
    """MFA setup verification form."""
    
    token = forms.CharField(
        max_length=6,
        min_length=6,
        label='Enter the code from your authenticator app',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': '000000',
            'autocomplete': 'off',
            'inputmode': 'numeric',
            'pattern': '[0-9]*'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('token', css_class='mb-3'),
            Submit('submit', 'Enable MFA', css_class='btn btn-success w-100')
        )


class UserRegistrationForm(UserCreationForm):
    """User registration form."""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('email', css_class='mb-3'),
            Row(
                Column(Field('first_name'), css_class='col-md-6 mb-3'),
                Column(Field('last_name'), css_class='col-md-6 mb-3'),
            ),
            Field('password1', css_class='mb-3'),
            Field('password2', css_class='mb-3'),
            Submit('submit', 'Register', css_class='btn btn-primary w-100')
        )
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class PasswordResetRequestForm(forms.Form):
    """Password reset request form."""
    
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('email', css_class='mb-3'),
            Submit('submit', 'Send Reset Link', css_class='btn btn-primary w-100')
        )


class CustomPasswordResetForm(SetPasswordForm):
    """Custom password reset form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('new_password1', css_class='mb-3'),
            Field('new_password2', css_class='mb-3'),
            Submit('submit', 'Reset Password', css_class='btn btn-primary w-100')
        )
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('old_password', css_class='mb-3'),
            Field('new_password1', css_class='mb-3'),
            Field('new_password2', css_class='mb-3'),
            Submit('submit', 'Change Password', css_class='btn btn-primary')
        )
        for field in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserProfileForm(forms.ModelForm):
    """User profile update form."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'avatar', 'position', 'department']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column(Field('first_name'), css_class='col-md-6 mb-3'),
                Column(Field('last_name'), css_class='col-md-6 mb-3'),
            ),
            Row(
                Column(Field('phone'), css_class='col-md-6 mb-3'),
                Column(Field('position'), css_class='col-md-6 mb-3'),
            ),
            Field('department', css_class='mb-3'),
            Field('avatar', css_class='mb-3'),
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        )
