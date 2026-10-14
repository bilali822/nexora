from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import (Service, WhyUs, ProcessStep, Stat, Testimonial, Client,
                     FAQ, PricingPlan, BlogPost, SiteSettings)
from .forms import ContactForm
from projects.models import Project


def home(request):
    return render(request, 'core/home.html', {
        'services': Service.objects.all(),
        'why_us': WhyUs.objects.all(),
        'process': ProcessStep.objects.all(),
        'stats': Stat.objects.all(),
        'projects': Project.objects.filter(is_featured=True)[:6],
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        'clients': Client.objects.all(),
        'faqs': FAQ.objects.filter(is_active=True)[:8],
        'pricing': PricingPlan.objects.prefetch_related('features'),
        'settings': SiteSettings.get(),
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'core/service_detail.html', {'service': service})


def services(request):
    return render(request, 'core/services.html', {'services': Service.objects.all()})


def about(request):
    return render(request, 'core/about.html', {
        'stats': Stat.objects.all(),
        'why_us': WhyUs.objects.all(),
        'process': ProcessStep.objects.all(),
    })


def pricing(request):
    return render(request, 'core/pricing.html', {
        'pricing': PricingPlan.objects.prefetch_related('features'),
        'faqs': FAQ.objects.filter(is_active=True),
    })


def blog_list(request):
    q = request.GET.get('q', '')
    posts = BlogPost.objects.filter(is_published=True)
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'core/blog_list.html', {'posts': posts, 'q': q})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    return render(request, 'core/blog_detail.html', {'post': post, 'related': related})


def privacy(request):
    return render(request, 'core/privacy.html')


def terms(request):
    return render(request, 'core/terms.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إرسال رسالتك، شكراً!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


def handler404(request, exception):
    return render(request, '404.html', status=404)
