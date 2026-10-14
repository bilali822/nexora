from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta


def custom_admin_index(request, extra_context=None):
    """يستبدل الصفحة الرئيسية للأدمن بـ Dashboard مخصص"""
    from core.models import Service, BlogPost, Testimonial
    from projects.models import Project
    from requests_app.models import ProjectRequest

    week_ago = timezone.now() - timedelta(days=7)
    month_ago = timezone.now() - timedelta(days=30)

    stats = {
        'total_requests': ProjectRequest.objects.count(),
        'new_requests': ProjectRequest.objects.filter(status='new').count(),
        'week_requests': ProjectRequest.objects.filter(created_at__gte=week_ago).count(),
        'month_requests': ProjectRequest.objects.filter(created_at__gte=month_ago).count(),
        'total_projects': Project.objects.count(),
        'featured_projects': Project.objects.filter(is_featured=True).count(),
        'total_services': Service.objects.count(),
        'total_posts': BlogPost.objects.count(),
        'total_testimonials': Testimonial.objects.count(),
    }

    # آخر 5 طلبات
    recent_requests = ProjectRequest.objects.order_by('-created_at')[:5]

    # حالة الطلبات
    status_counts = {
        'new': ProjectRequest.objects.filter(status='new').count(),
        'review': ProjectRequest.objects.filter(status='review').count(),
        'contacted': ProjectRequest.objects.filter(status='contacted').count(),
        'accepted': ProjectRequest.objects.filter(status='accepted').count(),
        'rejected': ProjectRequest.objects.filter(status='rejected').count(),
        'done': ProjectRequest.objects.filter(status='done').count(),
    }

    # أكثر المشاريع مشاهدة (لو عندك نظام views)
    top_projects = Project.objects.filter(is_featured=True)[:4]

    context = {
        **stats,
        'recent_requests': recent_requests,
        'status_counts': status_counts,
        'top_projects': top_projects,
        'title': 'لوحة التحكم',
    }
    if extra_context:
        context.update(extra_context)
    return render(request, 'admin/dashboard.html', context)
