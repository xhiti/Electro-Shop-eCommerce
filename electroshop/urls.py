"""electroshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    # super admin (only for developers)
    path('admin/', admin.site.urls),

    # users
    path('', views.index, name='index'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('category/', views.category, name='category'),
    path('blog/', include('blog.urls')),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # admin
    path('electroshop-admin/dashboard', views.admin_index, name='admin-index'),
    path('electroshop-admin/analytics', views.admin_analytics, name='admin-analytics'),
    path('electroshop-admin/sales', views.admin_sales, name='admin-sales'),
    path('electroshop-admin/products', views.admin_product_list, name='admin-products-list'),
    path('electroshop-admin/add-product', views.admin_add_product, name='admin-add-product'),
    path('electroshop-admin/categories', views.admin_categories_list, name='admin-categories-list'),
    path('electroshop-admin/add-category', views.admin_add_category, name='admin-add-category'),
    path('electroshop-admin/categories/edit/<slug:category_slug>/', views.edit_category, name='admin-edit-category'),
    path('electroshop-admin/categories/delete/<slug:category_slug>/', views.delete_category, name='admin-delete-category'),
    path('electroshop-admin/reviews', views.admin_reviews_list, name='admin-reviews-list'),
    path('electroshop-admin/reviews/delete/<slug:pk>/', views.delete_review, name='admin-delete-review'),
    path('electroshop-admin/customers', views.admin_customer_list, name='admin-customers-list'),
    path('electroshop-admin/customers/delete/<slug:pk>/', views.delete_customer, name='admin-delete-customer'),
    path('electroshop-admin/posts', views.admin_posts_list, name='admin-posts-list'),
    path('electroshop-admin/add-post', views.admin_add_post, name='admin-add-post'),
    path('electroshop-admin/posts/edit/<slug:pk>/', views.admin_edit_post, name='admin-edit-post'),
    path('electroshop-admin/posts/delete/<slug:pk>/', views.admin_delete_post, name='admin-delete-post'),
    path('electroshop-admin/orders', views.admin_orders_list, name='admin-orders-list'),
    path('electroshop-admin/orders/order-details/<slug:order_number>/', views.admin_view_invoice, name='admin-order-details'),
    path('electroshop-admin/orders/order-details/print/<slug:order_number>/', views.admin_print_invoice, name='admin-print-invoice'),

    # path('electroshop-admin/add-product', views.admin_add_product, name='admin-add-product'),

    path('electroshop-admin/error404', views.admin_error, name='admin-error-404'),
    path('electroshop-admin/maintenance', views.admin_maintenance, name='admin-maintenance'),
    path('electroshop-admin/invoice', views.admin_view_invoice, name='admin-view-invoice'),
    path('electroshop-admin/create-invoice', views.admin_create_invoice, name='admin-create-invoice'),
    path('electroshop-admin/profile', views.admin_user_profile, name='admin-user-profile'),

    # new updated urls
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
