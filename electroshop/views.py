from django.shortcuts import render
from store.models import Product
from category.models import Category


def index(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'index.html', context)


def category(request):
    return render(request, 'category.html')


def blog(request):
    return render(request, 'blog.html')


def about(request):
    return render(request, 'category.html')


def contact(request):
    return render(request, 'contact.html')
