from django.shortcuts import render
from .models import Blog


# Create your views here.
def blog(request):
    blogs = Blog.objects.order_by('-created_date').filter(is_active=True)

    context = {
        'blogs': blogs
    }

    return render(request, 'blog.html', context)


def edit_blog(request):
    blogs = Blog.objects.order_by('-created_date').filter(is_active=True)

    context = {
        'blogs': blogs
    }

    return render(request, 'blog.html', context)


def delete_blog(request):
    blogs = Blog.objects.order_by('-created_date').filter(is_active=True)

    context = {
        'blogs': blogs
    }

    return render(request, 'blog.html', context)
