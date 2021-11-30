from django.shortcuts import render
from store.models import Product
from category.models import Category
from store.models import ReviewRating
from orders.models import Order
from accounts.models import UserProfile, Account
from blog.models import Blog


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


def admin_sales(request):
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
    return render(request, 'electroshop_admin/sales.html', context)


def admin_product_list(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products
    }
    return render(request, 'electroshop_admin/products-list.html', context)


def admin_add_product(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all().filter(is_active=True)
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'electroshop_admin/add-product.html', context)


def admin_categories_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'electroshop_admin/categories-list.html', context)


def admin_add_category(request):
    categories = Category.objects.all().filter(is_active=True)
    context = {
        'categories': categories
    }
    return render(request, 'electroshop_admin/add-category.html', context)


def admin_reviews_list(request):
    reviews = ReviewRating.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'electroshop_admin/products-reviews.html', context)


def admin_orders_list(request):
    orders = Order.objects.filter().order_by('-created_at')
    no_products = Product.objects.all().count()
    no_orders = Order.objects.all().count()
    context = {
        'orders': orders,
        'no_products': no_products,
        'no_orders': no_orders
    }
    return render(request, 'electroshop_admin/orders-list.html', context)


def admin_customer_list(request):
    customers = Account.objects.filter(is_admin=False, is_super_admin=False)
    no_products = Product.objects.all().count()
    no_orders = Order.objects.all().count()
    context = {
        'customers': customers,
        'no_products': no_products,
        'no_orders': no_orders
    }
    return render(request, 'electroshop_admin/customers-list.html', context)


def admin_posts_list(request):
    posts = Blog.objects.all().filter(is_active=True)
    no_products = Product.objects.all().count()
    no_orders = Order.objects.all().count()
    context = {
        'posts': posts,
        'no_products': no_products,
        'no_orders': no_orders
    }
    return render(request, 'electroshop_admin/posts-list.html', context)


def admin_add_post(request):
    post = Blog.objects.all().filter(is_active=True)
    context = {
        'post': post
    }
    return render(request, 'electroshop_admin/add-post.html', context)


def admin_view_invoice(request):
    orders = Order.objects.filter().order_by('-created_at')
    no_products = Product.objects.all().count()
    no_orders = Order.objects.all().count()
    context = {
        'orders': orders,
        'no_products': no_products,
        'no_orders': no_orders
    }
    return render(request, 'electroshop_admin/view-invoice.html', context)


def admin_create_invoice(request):
    orders = Order.objects.filter().order_by('-created_at')
    no_products = Product.objects.all().count()
    no_orders = Order.objects.all().count()
    context = {
        'orders': orders,
        'no_products': no_products,
        'no_orders': no_orders
    }
    return render(request, 'electroshop_admin/create-invoice.html', context)


def admin_user_profile(request):
    orders = Order.objects.filter().order_by('-created_at')
    no_products = Product.objects.all().count()
    no_orders = Order.objects.all().count()
    context = {
        'orders': orders,
        'no_products': no_products,
        'no_orders': no_orders
    }
    return render(request, 'electroshop_admin/maintenance.html', context)


def admin_error(request):
    return render(request, 'electroshop_admin/error.html')


def admin_maintenance(request):
    return render(request, 'electroshop_admin/maintenance.html')
