import jingo

from django.shortcuts import get_object_or_404

from django_jobvite.models import Position, Category


def careers(request, slug=None):
    categories = Category.objects.all().order_by('name')
    return jingo.render(request, 'careers/home.html', {
        'categories': categories,
    })


def department(request, slug):
    category = get_object_or_404(Category, slug=slug)
    positions = Position.objects.filter(category=category).order_by('title')
    return jingo.render(request, 'careers/department.html', {
        'positions': positions,
        'category': category
    })


def position(request, job_id=None):
    position = get_object_or_404(Position, job_id=job_id)
    return jingo.render(request, 'careers/position.html', {
        'position': position,
    })


def benefits(request):
    return jingo.render(request, 'careers/benefits.html')
