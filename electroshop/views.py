from django.shortcuts import render
from store.models import Product
from category.models import Category
from store.models import ReviewRating
from orders.models import Order
from accounts.models import UserProfile


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


def admin_index(request):
    no_products = Product.objects.all().count()
    no_orders = Order.objects.all().count()
    no_clients = UserProfile.objects.all().count()

    orders = Order.objects.all().order_by('-created_at')[:5]

    context = {
        'no_products': no_products,
        'no_orders': no_orders,
        'no_clients': no_clients,
        'orders': orders
    }

    return render(request, 'electroshop_admin/index.html', context)


def admin_analytics(request):
    no_products = Product.objects.all().count()
    no_orders = Order.objects.all().count()
    no_clients = UserProfile.objects.all().count()
    no_ratings = ReviewRating.objects.all().count()

    orders = Order.objects.all().order_by('-created_at')[:5]
    products = Product.objects.all().order_by('stock')[:6]
    customers = UserProfile.objects.all().order_by('user__date_joined')[:5]
    ratings = ReviewRating.objects.all().order_by('-created_at')[:5]

    context = {
        'no_products': no_products,
        'no_orders': no_orders,
        'no_clients': no_clients,
        'no_ratings': no_ratings,
        'orders': orders,
        'products': products,
        'customers': customers,
        'ratings': ratings
    }

    return render(request, 'electroshop_admin/analytics.html', context)
