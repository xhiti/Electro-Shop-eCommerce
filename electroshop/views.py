from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from store.models import Product
from category.models import Category
from store.models import ReviewRating
from orders.models import Order, OrderProduct
from accounts.models import UserProfile, Account
from blog.models import Blog
from store.helpers.invoicePrinter import InvoicePrinter


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


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def admin_product_list(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products
    }
    return render(request, 'electroshop_admin/products-list.html', context)


@login_required(login_url='login')
def admin_add_product(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all().filter(is_active=True)
    context = {
        'products': products,
        'categories': categories
    }

    if request.method == 'POST':
        product_name = request.POST['product_name']
        if product_name is None or product_name == "":
            messages.error(request, "Product name can't be blank!")
        else:
            product_name = str(product_name).capitalize()
            slug = str(product_name).lower().replace(" ", "-")
            print("Product Name: " + str(product_name))
            print("Product Slug: " + str(slug))

        price = request.POST['price']
        if price is None or price == "":
            messages.error(request, "Product price can't be blank!")
        else:
            price = int(price)
            print("Product Price: " + str(price))

        category_name = request.POST['category_name']
        if category_name is None or category_name == "" or category_name == "0":
            messages.error(request, "Category can't be blank!")
        else:
            category_name = category_name
            print("Category ID: " + str(category_name))

        stock = request.POST['stock']
        if stock is None or stock == "":
            messages.error(request, "Product stock can't be blank!")
        else:
            stock = int(stock)
            print("Product Stock: " + str(stock))

        decription = request.POST['description']
        if decription is None or decription == "":
            decription = decription
        else:
            decription = decription
            print("Product Description: " + str(decription))

        image = request.POST['image']
        if image is None or image == "":
            image = image
        else:
            image = image

        counter = Product.objects.filter(product_name=product_name, slug=slug, is_available=True).count()
        if counter > 0:
            messages.error(request, "Product exists!")
        else:
            Product.objects.create(
                product_name=product_name,
                slug=slug,
                product_description=decription,
                price=price,
                stock=stock,
                image=image,
                category=get_object_or_404(Category, id=category_name)
            )
            messages.success(request, "Product added successfully!")
            return redirect('admin-products-list')
    return render(request, 'electroshop_admin/add-product.html', context)


@login_required(login_url='login')
def admin_edit_product(request, product_slug=None):
    product_details = Product.objects.filter(id=product_slug, is_available=True).first()

    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all().filter(is_active=True)
    context = {
        'products': products,
        'categories': categories,
        'product_details': product_details
    }

    current_slug = product_details.slug
    current_category = product_details.category.category_name
    print("Current Category: " + str(current_category))


    if request.method == 'POST':
        product_name = request.POST['product_name']
        if product_name is None or product_name == "":
            messages.error(request, "Product name can't be blank!")
        else:
            product_name = str(product_name).capitalize()
            slug = str(product_name).lower().replace(" ", "-")
            print("Product Name: " + str(product_name))
            print("Product Slug: " + str(slug))

        price = request.POST['price']
        if price is None or price == "":
            messages.error(request, "Product price can't be blank!")
        else:
            price = int(price)
            print("Product Price: " + str(price))

        category_name = request.POST['category_name']
        if category_name is None or category_name == "" or category_name == "0":
            messages.error(request, "Category can't be blank!")
        else:
            category_name = category_name
            new_category = get_object_or_404(Category, id=category_name)
            print("Category ID: " + str(category_name))
            print("Category Name: " + str(new_category.category_name))

        stock = request.POST['stock']
        if stock is None or stock == "":
            messages.error(request, "Product stock can't be blank!")
        else:
            stock = int(stock)
            print("Product Stock: " + str(stock))

        decription = request.POST['description']
        if decription is None or decription == "":
            decription = decription
        else:
            decription = decription
            print("Product Description: " + str(decription))

        image = request.POST['image']
        if image is None or image == "":
            image = image
        else:
            image = image

        counter = Product.objects.filter(product_name=product_name, is_available=True).exclude(
            id=product_slug).count()
        if counter > 0:
            messages.error(request, "Product exists!")
        else:
            Product.objects.filter(
                slug=current_slug
            ).update(
                product_name=product_name,
                slug=slug,
                product_description=decription,
                price=price,
                stock=stock,
                image=image,
                category=get_object_or_404(Category, id=category_name)
            )
            messages.success(request, "Product edited successfully!")
            return redirect('admin-products-list')
    return render(request, 'electroshop_admin/edit-product.html', context)


@login_required(login_url='login')
def delete_product(request, product_slug=None):
    if product_slug is not None:
        Product.objects.filter(id=product_slug, is_available=True).delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('admin-products-list')
    return render(request, 'electroshop_admin/products-list.html')


@login_required(login_url='login')
def admin_categories_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'electroshop_admin/categories-list.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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
        if description is None or description == "":
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


@login_required(login_url='login')
def delete_category(request, category_slug=None):
    if category_slug is not None:
        Category.objects.filter(slug=category_slug, is_active=True).delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('admin-categories-list')
    return render(request, 'electroshop_admin/categories-list.html')


@login_required(login_url='login')
def admin_reviews_list(request):
    reviews = ReviewRating.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'electroshop_admin/products-reviews.html', context)


@login_required(login_url='login')
def delete_review(request, pk=None):
    if pk is not None:
        ReviewRating.objects.filter(id=pk).delete()
        messages.success(request, "Review deleted successfully!")
        return redirect('admin-reviews-list')
    return render(request, 'electroshop_admin/products-reviews-list.html')


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_customer(request, pk=None):
    if pk is not None:
        Account.objects.filter(id=pk).delete()
        messages.success(request, "Customer deleted successfully!")
        return redirect('admin-customers-list')
    return render(request, 'electroshop_admin/customers-list.html')


@login_required(login_url='login')
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


@login_required(login_url='login')
def admin_add_post(request):

    categories = Category.objects.all().filter(is_active=True)

    if request.method == 'POST':
        title = request.POST['title']
        if title is None or title == "":
            messages.error(request, "Post title name can't be blank!")
        else:
            title = str(title).capitalize()
            slug = str(title).lower().replace(" ", "-")

        description = request.POST['description']
        if description is None or description == "":
            description = str(description + "")
        else:
            description = str(description).capitalize()

        image = request.POST['image']
        if image is None or image == "":
            image = image
        else:
            image = image

        counter = Blog.objects.filter(title=title, is_active=True).count()
        if counter > 0:
            messages.error(request, "Post exists!")
        else:
            print("Blog created!!")
            Blog.objects.create(
                title=title,
                description=description,
                blog_image=image,
                is_active=True
            )
            messages.success(request, "Post added successfully!")
            return redirect('admin-posts-list')

    context = {
        'categories': categories
    }

    return render(request, 'electroshop_admin/add-post.html', context)


@login_required(login_url='login')
def admin_edit_post(request, pk=None):
    post_details = Blog.objects.filter(id=pk, is_active=True).first()

    context = {
        'post_details': post_details
    }

    if request.method == 'POST':
        title = request.POST['title']
        if title is None or v == "":
            messages.error(request, "Post title can't be blank!")
        else:
            title = str(title).capitalize()

        description = request.POST['description']
        if description is None or description == "":
            description = str(description + "")
        else:
            description = str(description).capitalize()

        image = request.POST['image']
        if image is None or image == "":
            image = image
        else:
            image = image

        counter = Blog.objects.filter(title=title, is_active=True).exclude(id=pk).count()
        if counter > 0:
            messages.error(request, "Post exists!")
        else:
            Blog.objects.filter(
                id=pk
            ).update(
                title=title,
                description=description,
                blog_image=image
            )
            messages.success(request, "Post updated successfully!")
            return redirect('admin-posts-list')
    return render(request, 'electroshop_admin/edit-post.html', context)


def admin_delete_post(request, pk=None):
    if pk is not None:
        Blog.objects.filter(id=pk).delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('admin-posts-list')
    return render(request, 'electroshop_admin/posts-list.html')


@login_required(login_url='login')
def admin_orders_list(request):
    orders = Order.objects.all().order_by('-created_at')
    no_products = Product.objects.all().count()
    no_orders = Order.objects.all().count()
    context = {
        'orders': orders,
        'no_products': no_products,
        'no_orders': no_orders
    }
    return render(request, 'electroshop_admin/orders-list.html', context)


@login_required(login_url='login')
def admin_view_invoice(request, order_number=None):

    context = {

    }

    if order_number is not None:
        order_details = Order.objects.filter(order_number=order_number).first()
        order_details_items = OrderProduct.objects.filter(order__order_number=order_number)

        sub_total = 0

        for i in order_details_items:
            sub_total += i.product_price * i.quantity

        context = {
            'order_details': order_details,
            'order_details_items': order_details_items,
            'sub_total': sub_total
        }
    return render(request, 'electroshop_admin/view-invoice.html', context)


@login_required(login_url='login')
def admin_print_invoice(request, order_number=None):
    if order_number is not None:
        order_details = Order.objects.filter(order_number=order_number).first()
        order_details_items = OrderProduct.objects.filter(order__order_number=order_number)

        sub_total = 0

        for i in order_details_items:
            sub_total += i.product_price * i.quantity

        return InvoicePrinter.printInvoice(order_details, order_details_items, sub_total)


@login_required(login_url='login')
def admin_create_invoice(request):
    return render(request, 'electroshop_admin/create-invoice.html')


@login_required(login_url='login')
def admin_user_profile(request):
    return render(request, 'electroshop_admin/maintenance.html')


@login_required(login_url='login')
def admin_error(request):
    return render(request, 'electroshop_admin/error.html')


@login_required(login_url='login')
def admin_maintenance(request):
    return render(request, 'electroshop_admin/maintenance.html')
