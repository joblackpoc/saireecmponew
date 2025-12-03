# SaiReeCMPO - Government Office CMS

A comprehensive Django 5+ Content Management System for government offices with advanced security features, blog system, file downloads, and PDF conversion capabilities.

## Features

### 🔐 Security & Authentication
- Custom user model with email-based authentication
- Multi-Factor Authentication (MFA) with Google Authenticator
- Backup codes for MFA recovery (10 codes)
- Password reset with 24-hour token expiry
- Login attempt tracking with IP and user agent
- Failed login attempt counter
- Session security with 24-hour expiry

### 📄 Content Management
- **Site Settings**: Global site configuration
- **Navbar Menu**: Hierarchical menu management
- **Hero Slides**: Carousel slider for homepage
- **About Sections**: Multiple about sections with CKEditor
- **Vision/Mission/Values**: Type-based content blocks
- **Team Members**: Staff profiles with social links
- **Announcements**: News with priority levels and expiry
- **Activities**: Events with photo galleries
- **Locations**: Office locations with Google Maps embed
- **Contact Form**: Public contact with admin management
- **Features**: Highlight boxes for homepage

### 📝 Blog System
- Blog posts with categories and tags
- Rich text editing with CKEditor 5
- Comment system with approval workflow
- Featured posts and view count tracking
- Search and category filtering

### 📥 Download Management
- Support for PDF, DOCX, XLSX, PPTX, ZIP, RAR files
- File categories
- Download tracking and logging
- PDF inline viewer

### 🔄 PDF Converter
- Convert DOCX to PDF
- Convert PPTX to PDF
- Export to HTML with style preservation
- Conversion history and logs

## Installation

### Prerequisites
- Python 3.10+
- pip
- LibreOffice (for PDF conversion)

### Setup

1. **Clone or extract the project**
```bash
cd saireecmponew
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Collect static files** (for production)
```bash
python manage.py collectstatic
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the site**
- Main site: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- Dashboard: http://localhost:8000/accounts/dashboard/

## Configuration

### Environment Variables (for production)

Edit `core/settings.py`:

```python
# Generate a new secret key for production
SECRET_KEY = 'your-production-secret-key'

# Disable debug mode
DEBUG = False

# Add your domain
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database (PostgreSQL recommended for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Security Settings

Uncomment these in `core/settings.py` for production:

```python
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## Project Structure

```
saireecmponew/
├── core/                   # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # User authentication & MFA
├── content/                # Content management
├── blog/                   # Blog system
├── download/               # File downloads
├── pdfapp/                 # PDF converter
├── templates/              # HTML templates
│   ├── accounts/
│   ├── content/
│   ├── blog/
│   ├── download/
│   ├── pdfapp/
│   └── dashboard/
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploads
├── requirements.txt
└── manage.py
```

## Dashboard Routes

| URL | Description |
|-----|-------------|
| `/accounts/dashboard/` | Main dashboard |
| `/accounts/profile/` | User profile & password |
| `/accounts/mfa/setup/` | Enable MFA |
| Dashboard Content Management |
| `/content/dashboard/settings/` | Site settings |
| `/content/dashboard/navbar/` | Navbar menu |
| `/content/dashboard/hero/` | Hero slides |
| `/content/dashboard/about/` | About sections |
| `/content/dashboard/vmv/` | Vision/Mission/Values |
| `/content/dashboard/team/` | Team members |
| `/content/dashboard/announcements/` | Announcements |
| `/content/dashboard/activities/` | Activities |
| `/content/dashboard/features/` | Features |
| `/content/dashboard/locations/` | Locations |
| `/content/dashboard/contacts/` | Contact messages |
| Blog Management |
| `/blog/dashboard/` | Blog posts |
| `/blog/dashboard/categories/` | Categories |
| `/blog/dashboard/tags/` | Tags |
| `/blog/dashboard/comments/` | Comments |
| Download Management |
| `/download/dashboard/` | Download files |
| `/download/dashboard/categories/` | Categories |
| `/download/dashboard/logs/` | Download logs |
| PDF Converter |
| `/pdf/` | PDF documents |
| `/pdf/upload/` | Upload & convert |

## Technologies

- **Backend**: Django 5.2+
- **Frontend**: Bootstrap 3 (template), Bootstrap 5 (dashboard)
- **Rich Text**: CKEditor 5
- **Forms**: Crispy Forms + Bootstrap 5
- **MFA**: PyOTP + QRCode
- **PDF**: ReportLab, python-docx, python-pptx

## License

MIT License

## Support

For support, please contact the development team.
