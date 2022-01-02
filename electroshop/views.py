from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
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


# @login_required(login_url='login')
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


# @login_required(login_url='login')
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


# @login_required(login_url='login')
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


# @login_required(login_url='login')
def admin_product_list(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products
    }
    return render(request, 'electroshop_admin/products-list.html', context)


# @login_required(login_url='login')
def admin_add_product(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all().filter(is_active=True)
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'electroshop_admin/add-product.html', context)


# @login_required(login_url='login')
def admin_categories_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'electroshop_admin/categories-list.html', context)


# @login_required(login_url='login')
def admin_add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        if category_name is None or category_name == "":
            messages.error(request, "Category name can't be blank!")
        else:
            category_name = str(category_name).capitalize()
            slug = str(category_name).lower().replace(" ", "-")

        description = request.POST['description']
        if category_name is None or category_name == "":
            description = str(description + "")
        else:
            description = str(description).capitalize()

        image = request.POST['image']
        if image is None or image == "":
            image = image
        else:
            image = image

        counter = Category.objects.filter(category_name=category_name, is_active=True).count()
        if counter > 0:
            messages.error(request, "Category exists!")
        else:
            Category.objects.create(
                category_name=category_name,
                description=description,
                category_image=image,
                slug=slug
            )
            messages.success(request, "Category added successfully!")
            return redirect('admin-categories-list')
    return render(request, 'electroshop_admin/add-category.html')


def edit_category(request, category_slug=None):

    category_details = Category.objects.filter(slug=category_slug, is_active=True).first()

    context = {
        'category_details': category_details
    }

    current_slug = category_details.slug

    if request.method == 'POST':
        category_name = request.POST['category_name']
        if category_name is None or category_name == "":
            messages.error(request, "Category name can't be blank!")
        else:
            category_name = str(category_name).capitalize()
            slug = str(category_name).lower().replace(" ", "-")

        description = request.POST['description']
        if category_name is None or category_name == "":
            description = str(description + "")
        else:
            description = str(description).capitalize()

        image = request.POST['image']
        if image is None or image == "":
            image = image
        else:
            image = image

        counter = Category.objects.filter(category_name=category_name, is_active=True).exclude(slug=category_slug).count()
        if counter > 0:
            messages.error(request, "Category exists!")
        else:
            Category.objects.filter(
                slug=current_slug
            ).update(
                category_name=category_name,
                description=description,
                category_image=image,
                slug=slug
            )
            messages.success(request, "Category updated successfully!")
            return redirect('admin-categories-list')
    return render(request, 'electroshop_admin/edit-category.html', context)


def delete_category(request, category_slug=None):
    if category_slug is not None:
        Category.objects.filter(slug=category_slug, is_active=True).delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('admin-categories-list')
    return render(request, 'electroshop_admin/categories-list.html')


# @login_required(login_url='login')
def admin_reviews_list(request):
    reviews = ReviewRating.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'electroshop_admin/products-reviews.html', context)


# @login_required(login_url='login')
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


# @login_required(login_url='login')
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


# @login_required(login_url='login')
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


# @login_required(login_url='login')
def admin_add_post(request):
    post = Blog.objects.all().filter(is_active=True)
    context = {
        'post': post
    }
    return render(request, 'electroshop_admin/add-post.html', context)


# @login_required(login_url='login')
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


# @login_required(login_url='login')
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


# @login_required(login_url='login')
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


# @login_required(login_url='login')
def admin_error(request):
    return render(request, 'electroshop_admin/error.html')


# @login_required(login_url='login')
def admin_maintenance(request):
    return render(request, 'electroshop_admin/maintenance.html')
