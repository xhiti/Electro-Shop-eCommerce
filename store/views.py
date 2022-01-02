from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, ReviewRating, PrdouctGallery
from django.template import loader
from django.template.loader import get_template
from category.models import Category
from carts.views import _cart_id
from django.http import HttpResponse
from carts.models import Cart, CartItem
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from orders.models import OrderProduct
from .forms import ReviewForms
from .models import ReviewRating
from accounts.models import UserProfile


# Create your views here.
def store(request, category_slug=None):

    paged_products = None
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        products = products.order_by('?')
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('?')
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'categories': categories,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()
    except Exception as exc:
        raise exc

    products = Product.objects.all().filter(is_available=True)

    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()

        except OrderProduct.DoesNotExist:
            order_product = None

    else:
        order_product = None

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    product_gallery = PrdouctGallery.objects.filter(product_id=single_product.id)

    user_profile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'single_product': single_product,
        'products': products,
        'in_cart': in_cart,
        'order_product': order_product,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'user_profile': user_profile
    }

    return render(request, 'store/product_detail.html', context)


def search(request):
    products = None
    search_products_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            search_products_count = products.count()

    context = {
        'products': products,
        'search_products_count': search_products_count,
    }

    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    current_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForms(request.POST, instance=reviews)

            form.save()
            messages.success(request, 'Thank You: Your review has been updated!')

            return redirect(current_url)

        except ReviewRating.DoesNotExist:
            form = ReviewForms(request.POST)

            if form.is_valid():
                data = ReviewRating()
                data.subject = 'Subject'
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id

                data.save()

                messages.success(request, 'Thank You: Your review has been submited!')

                return redirect(current_url)
    return


def product_xml_report(request):
    products = Product.objects.filter(is_available=True).order_by('product_name')
    template = loader.get_template('xml/products.xml')
    context = {
        'products': products
    }
    return HttpResponse(template.render(context))


def delete_category(request, pk):
    return


def edit_category(request, pk):
    return


def edit_product(request, pk):
    return


def delete_product(request, pk):
    return
