import jingo

from django.shortcuts import get_object_or_404

from django_jobvite.models import Position, Category


def careers(request, slug=None):
    categories = Category.objects.all()
    return jingo.render(request, 'careers/home.html', {
        'categories': categories,
    })


def department(request, slug):
    selected = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    positions = Position.objects.filter(category=selected)
    return jingo.render(request, 'careers/home.html', {
        'categories': categories,
        'positions': positions,
        'selected': selected,
    })


def position(request, job_id=None):
    position = get_object_or_404(Position, job_id=job_id)
    return jingo.render(request, 'careers/home.html', {
        'position': position,
    })
