"""
Blog app models.
Blog posts with CKEditor 5 content, images, and video embeds.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    """Blog category."""
    
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Blog tag."""
    
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Blog post model."""
    
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    short_description = models.TextField(_('short description'), max_length=500)
    description = CKEditor5Field(_('content'), config_name='extends')
    image = models.ImageField(_('featured image'), upload_to='blog/')
    video_embed = models.TextField(
        _('video embed code'),
        blank=True,
        help_text=_('Paste YouTube or Vimeo embed code here')
    )
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='posts',
        verbose_name=_('category')
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name=_('tags'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name=_('author')
    )
    
    is_published = models.BooleanField(_('is published'), default=False)
    is_featured = models.BooleanField(_('is featured'), default=False)
    view_count = models.PositiveIntegerField(_('view count'), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(_('published at'), null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set published_at when first published
        if self.is_published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)


class BlogComment(models.Model):
    """Blog comment model."""
    
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'))
    content = models.TextField(_('comment'))
    is_approved = models.BooleanField(_('is approved'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
