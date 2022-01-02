from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Blog


# Create your views here.
def blog(request):
    blogs = Blog.objects.order_by('-created_date').filter(is_active=True)

    context = {
        'blogs': blogs
    }

    return render(request, 'blog.html', context)


@login_required(login_url='login')
def edit_blog(request):
    blogs = Blog.objects.order_by('-created_date').filter(is_active=True)

    context = {
        'blogs': blogs
    }

    return render(request, 'blog.html', context)


@login_required(login_url='login')
def delete_blog(request):
    blogs = Blog.objects.order_by('-created_date').filter(is_active=True)

    context = {
        'blogs': blogs
    }

    return render(request, 'blog.html', context)
