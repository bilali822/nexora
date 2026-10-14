from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list(request):
    category = request.GET.get('category')
    qs = Project.objects.all()
    if category:
        qs = qs.filter(category=category)
    return render(request, 'projects/list.html', {
        'projects': qs,
        'active_category': category,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(category=project.category).exclude(pk=project.pk)[:3]
    return render(request, 'projects/detail.html', {
        'project': project,
        'related': related,
    })
