from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    cart.save()

    if current_user.is_authenticated:

        try:
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity += 1

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)

        cart_item.save()

        return redirect('cart')

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)

        cart_item.save()

        return redirect('cart')


def remove_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass

    return redirect('cart')


def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    cart_items_count = 0

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        cart_items_count = cart_items.count()

        for car_item in cart_items:
            total += (car_item.product.price * car_item.quantity)
            quantity += car_item.quantity

        tax = (5 * total)/100
        grand_total = total + tax

    except:
        pass

    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'cart_items_count': cart_items_count,
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 1
    grand_total = 0
    cart_items_count = 0

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for car_item in cart_items:
            total += (car_item.product.price * car_item.quantity)
            quantity += car_item.quantity

        tax = (5 * total) / 100
        grand_total = total + tax

    except:
        pass

    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'cart_items_count': cart_items_count,
    }

    return render(request, 'store/checkout.html', context)
