"""
Blog app views.
Public blog pages and dashboard management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import BlogPost, Category, Tag, BlogComment
from .forms import BlogPostForm, CategoryForm, TagForm, BlogCommentForm


# Public Views
class BlogListView(ListView):
    """Public blog listing."""
    
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        
        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(short_description__icontains=query)
            )
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Tag filter
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['tags'] = Tag.objects.all()
        context['featured_posts'] = BlogPost.objects.filter(is_published=True, is_featured=True)[:5]
        return context


class BlogDetailView(DetailView):
    """Blog post detail view."""
    
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = BlogCommentForm()
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['related_posts'] = BlogPost.objects.filter(
            is_published=True,
            category=self.object.category
        ).exclude(pk=self.object.pk)[:4]
        context['categories'] = Category.objects.filter(is_active=True)
        return context


def blog_comment_submit(request, pk):
    """Handle blog comment submission."""
    
    post = get_object_or_404(BlogPost, pk=pk, is_published=True)
    
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
        else:
            messages.error(request, 'Please correct the errors in your comment.')
    
    return redirect('blog:detail', slug=post.slug)


# Dashboard Views
class DashboardBlogListView(LoginRequiredMixin, ListView):
    """Dashboard blog post listing."""
    
    model = BlogPost
    template_name = 'dashboard/blog_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog'
        return context


class DashboardBlogCreateView(LoginRequiredMixin, CreateView):
    """Dashboard blog post create."""
    
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('blog:dashboard_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Blog post created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog'
        context['title'] = 'Add Blog Post'
        return context


class DashboardBlogUpdateView(LoginRequiredMixin, UpdateView):
    """Dashboard blog post update."""
    
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('blog:dashboard_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog'
        context['title'] = 'Edit Blog Post'
        return context


class DashboardBlogDeleteView(LoginRequiredMixin, DeleteView):
    """Dashboard blog post delete."""
    
    model = BlogPost
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('blog:dashboard_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post deleted successfully!')
        return super().form_valid(form)


# Category Dashboard Views
class DashboardCategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard/category_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog_categories'
        return context


class DashboardCategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('blog:dashboard_category_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog_categories'
        context['title'] = 'Add Category'
        return context


class DashboardCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('blog:dashboard_category_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog_categories'
        context['title'] = 'Edit Category'
        return context


class DashboardCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('blog:dashboard_category_list')


# Tag Dashboard Views
class DashboardTagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'dashboard/tag_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog_tags'
        return context


class DashboardTagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('blog:dashboard_tag_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog_tags'
        context['title'] = 'Add Tag'
        return context


class DashboardTagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('blog:dashboard_tag_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog_tags'
        context['title'] = 'Edit Tag'
        return context


class DashboardTagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('blog:dashboard_tag_list')


# Comment Dashboard Views
class DashboardCommentListView(LoginRequiredMixin, ListView):
    model = BlogComment
    template_name = 'dashboard/comment_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'blog_comments'
        return context


@login_required
def dashboard_comment_approve(request, pk):
    """Approve a comment."""
    
    comment = get_object_or_404(BlogComment, pk=pk)
    comment.is_approved = True
    comment.save()
    messages.success(request, 'Comment approved successfully!')
    return redirect('blog:dashboard_comment_list')


class DashboardCommentDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogComment
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('blog:dashboard_comment_list')
