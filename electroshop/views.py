from django.shortcuts import render
from store.models import Product
from category.models import Category
from store.models import ReviewRating


def index(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'index.html', context)


def category(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    ratings = ReviewRating.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'ratings': ratings
    }

    return render(request, 'category.html', context)


def about(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    ratings = ReviewRating.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'ratings': ratings
    }

    return render(request, 'category.html', context)


def contact(request):
    return render(request, 'contact.html')
