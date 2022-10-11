from django.urls import path
from .views import (
    add_to_cart_page, 
    display_cart_page, 
    payment_page,
    display_thanks_page,
    display_payment_respone_page,
    delete_cart_item_page,
    display_checkout_page)

app_name = 'cart'

urlpatterns = [
    path('user/cart', display_cart_page, name='display'),
    path('add/to/cart/<int:product_id>', add_to_cart_page, name='add_to_cart'),
    path('payment/cart/<int:cart_id>', payment_page, name='payment'),
    path('thanks-page', display_thanks_page, name='thanks_page'),
    path('response', display_payment_respone_page, name='response'),
    path('delete', delete_cart_item_page, name='delete'),
    path('checkout', display_checkout_page, name='checkout')
]
