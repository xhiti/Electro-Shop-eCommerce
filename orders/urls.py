from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
]

urlpatterns += [
    path('orders/xml/', views.order_xml_report, name='order-xml-report')
]