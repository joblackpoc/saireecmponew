"""
Content app views.
Landing page and dashboard management views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q

from .models import (
    SiteSettings, NavbarMenu, HeroSlide, AboutSection, VisionMissionValue,
    TeamMember, Announcement, Activity, ActivityGallery, Location, 
    ContactMessage, Feature
)
from .forms import (
    SiteSettingsForm, NavbarMenuForm, HeroSlideForm, AboutSectionForm,
    VisionMissionValueForm, TeamMemberForm, AnnouncementForm, ActivityForm,
    LocationForm, ContactMessageForm, FeatureForm
)


def landing_page(request):
    """Main landing page view."""
    
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True),
        'features': Feature.objects.filter(is_active=True),
        'about_sections': AboutSection.objects.filter(is_active=True),
        'vision': VisionMissionValue.objects.filter(type='vision', is_active=True).first(),
        'mission': VisionMissionValue.objects.filter(type='mission', is_active=True).first(),
        'values': VisionMissionValue.objects.filter(type='value', is_active=True),
        'team_members': TeamMember.objects.filter(is_active=True),
        'announcements': Announcement.objects.filter(is_active=True)[:6],
        'activities': Activity.objects.filter(is_active=True)[:6],
        'location': Location.objects.filter(is_active=True, is_main=True).first(),
        'locations': Location.objects.filter(is_active=True),
        'contact_form': ContactMessageForm(),
    }
    
    return render(request, 'content/landing.html', context)


def contact_submit(request):
    """Handle contact form submission."""
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('content:landing')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('content:landing')


def announcement_detail(request, pk):
    """Announcement detail view."""
    
    announcement = get_object_or_404(Announcement, pk=pk, is_active=True)
    announcement.view_count += 1
    announcement.save()
    
    return render(request, 'content/announcement_detail.html', {
        'announcement': announcement,
        'recent_announcements': Announcement.objects.filter(is_active=True).exclude(pk=pk)[:5]
    })


def activity_detail(request, pk):
    """Activity detail view."""
    
    activity = get_object_or_404(Activity, pk=pk, is_active=True)
    activity.view_count += 1
    activity.save()
    
    return render(request, 'content/activity_detail.html', {
        'activity': activity,
        'gallery': activity.gallery.all(),
        'recent_activities': Activity.objects.filter(is_active=True).exclude(pk=pk)[:5]
    })


def announcements_list(request):
    """List all announcements."""
    
    announcements = Announcement.objects.filter(is_active=True)
    query = request.GET.get('q')
    if query:
        announcements = announcements.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query)
        )
    
    return render(request, 'content/announcements_list.html', {
        'announcements': announcements
    })


def activities_list(request):
    """List all activities."""
    
    activities = Activity.objects.filter(is_active=True)
    query = request.GET.get('q')
    if query:
        activities = activities.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query)
        )
    
    return render(request, 'content/activities_list.html', {
        'activities': activities
    })


# Dashboard Views
class DashboardMixin(LoginRequiredMixin):
    """Mixin for dashboard views."""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module_name
        return context


# Site Settings Dashboard
@login_required
def dashboard_site_settings(request):
    """Site settings dashboard."""
    
    settings_obj = SiteSettings.get_settings()
    
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings updated successfully!')
            return redirect('content:dashboard_site_settings')
    else:
        form = SiteSettingsForm(instance=settings_obj)
    
    return render(request, 'dashboard/site_settings.html', {
        'form': form,
        'module': 'settings'
    })


# Navbar Menu Dashboard
class NavbarMenuListView(LoginRequiredMixin, ListView):
    model = NavbarMenu
    template_name = 'dashboard/navbar_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'navbar'
        return context


class NavbarMenuCreateView(LoginRequiredMixin, CreateView):
    model = NavbarMenu
    form_class = NavbarMenuForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_navbar_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'navbar'
        context['title'] = 'Add Menu Item'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Menu item created successfully!')
        return super().form_valid(form)


class NavbarMenuUpdateView(LoginRequiredMixin, UpdateView):
    model = NavbarMenu
    form_class = NavbarMenuForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_navbar_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'navbar'
        context['title'] = 'Edit Menu Item'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Menu item updated successfully!')
        return super().form_valid(form)


class NavbarMenuDeleteView(LoginRequiredMixin, DeleteView):
    model = NavbarMenu
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_navbar_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'navbar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Menu item deleted successfully!')
        return super().form_valid(form)


# Hero Slides Dashboard
class HeroSlideListView(LoginRequiredMixin, ListView):
    model = HeroSlide
    template_name = 'dashboard/hero_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'hero'
        return context


class HeroSlideCreateView(LoginRequiredMixin, CreateView):
    model = HeroSlide
    form_class = HeroSlideForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_hero_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'hero'
        context['title'] = 'Add Hero Slide'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Hero slide created successfully!')
        return super().form_valid(form)


class HeroSlideUpdateView(LoginRequiredMixin, UpdateView):
    model = HeroSlide
    form_class = HeroSlideForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_hero_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'hero'
        context['title'] = 'Edit Hero Slide'
        return context


class HeroSlideDeleteView(LoginRequiredMixin, DeleteView):
    model = HeroSlide
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_hero_list')


# About Section Dashboard
class AboutSectionListView(LoginRequiredMixin, ListView):
    model = AboutSection
    template_name = 'dashboard/about_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'about'
        return context


class AboutSectionCreateView(LoginRequiredMixin, CreateView):
    model = AboutSection
    form_class = AboutSectionForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_about_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'about'
        context['title'] = 'Add About Section'
        return context


class AboutSectionUpdateView(LoginRequiredMixin, UpdateView):
    model = AboutSection
    form_class = AboutSectionForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_about_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'about'
        context['title'] = 'Edit About Section'
        return context


class AboutSectionDeleteView(LoginRequiredMixin, DeleteView):
    model = AboutSection
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_about_list')


# Vision/Mission/Values Dashboard
class VMVListView(LoginRequiredMixin, ListView):
    model = VisionMissionValue
    template_name = 'dashboard/vmv_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'vmv'
        return context


class VMVCreateView(LoginRequiredMixin, CreateView):
    model = VisionMissionValue
    form_class = VisionMissionValueForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_vmv_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'vmv'
        context['title'] = 'Add Vision/Mission/Value'
        return context


class VMVUpdateView(LoginRequiredMixin, UpdateView):
    model = VisionMissionValue
    form_class = VisionMissionValueForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_vmv_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'vmv'
        context['title'] = 'Edit Vision/Mission/Value'
        return context


class VMVDeleteView(LoginRequiredMixin, DeleteView):
    model = VisionMissionValue
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_vmv_list')


# Team Members Dashboard
class TeamMemberListView(LoginRequiredMixin, ListView):
    model = TeamMember
    template_name = 'dashboard/team_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'team'
        return context


class TeamMemberCreateView(LoginRequiredMixin, CreateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_team_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'team'
        context['title'] = 'Add Team Member'
        return context


class TeamMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_team_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'team'
        context['title'] = 'Edit Team Member'
        return context


class TeamMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = TeamMember
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_team_list')


# Announcements Dashboard
class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/announcement_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'announcements'
        return context


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_announcement_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'announcements'
        context['title'] = 'Add Announcement'
        return context


class AnnouncementUpdateView(LoginRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_announcement_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'announcements'
        context['title'] = 'Edit Announcement'
        return context


class AnnouncementDeleteView(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_announcement_list')


# Activities Dashboard
class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'dashboard/activity_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'activities'
        return context


class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_activity_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'activities'
        context['title'] = 'Add Activity'
        return context


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_activity_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'activities'
        context['title'] = 'Edit Activity'
        return context


class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_activity_list')


# Locations Dashboard
class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'dashboard/location_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'locations'
        return context


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_location_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'locations'
        context['title'] = 'Add Location'
        return context


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_location_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'locations'
        context['title'] = 'Edit Location'
        return context


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_location_list')


# Contact Messages Dashboard
class ContactMessageListView(LoginRequiredMixin, ListView):
    model = ContactMessage
    template_name = 'dashboard/contact_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'contacts'
        return context


class ContactMessageDetailView(LoginRequiredMixin, DetailView):
    model = ContactMessage
    template_name = 'dashboard/contact_detail.html'
    context_object_name = 'message'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.is_read = True
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'contacts'
        return context


class ContactMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = ContactMessage
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_contact_list')


# Features Dashboard
class FeatureListView(LoginRequiredMixin, ListView):
    model = Feature
    template_name = 'dashboard/feature_list.html'
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'features'
        return context


class FeatureCreateView(LoginRequiredMixin, CreateView):
    model = Feature
    form_class = FeatureForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_feature_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'features'
        context['title'] = 'Add Feature'
        return context


class FeatureUpdateView(LoginRequiredMixin, UpdateView):
    model = Feature
    form_class = FeatureForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('content:dashboard_feature_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = 'features'
        context['title'] = 'Edit Feature'
        return context


class FeatureDeleteView(LoginRequiredMixin, DeleteView):
    model = Feature
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('content:dashboard_feature_list')
