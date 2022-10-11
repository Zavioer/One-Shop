import time
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem
from product.models import Product
from .utils import create_payment_chk, send_bill_email


# Create your views here.
def add_to_cart_page(request, product_id):
    user_cart, new_user_cart = Cart.objects.get_or_create(user=request.user, status='ACTIVE')
    product = Product.objects.get(pk=product_id)

    if user_cart:
        # Increasing amount of product
        exist = CartItem.objects.filter(cart_id=user_cart.id, product_id=product.id).first()
         
        if exist:
            new_cart_item = exist
            new_cart_item.amount += 1
        else:
            new_cart_item = CartItem(cart=user_cart, product=product)
    else:
        new_cart_item = CartItem(cart=new_user_cart, product=product)

    new_cart_item.save()

    return redirect('product:home')

def display_cart_page(request):
    SHIPPING = 10
    # TODO
    # Change this approach of taking products to left join test this solution
    user_cart = Cart.objects.get(user=request.user, status='ACTIVE')
    cart_items = CartItem.objects.select_related('product').filter(cart=user_cart)
    print(cart_items.query)
    products = []
    total_price = 0

    for cart_item in cart_items:
        products.append(cart_item)
        total_price += cart_item.product.price * cart_item.amount
        
    context = {
        'cart_items': products,
        'cart': user_cart,
        'total_price': total_price,
        'currency': 'zł',
        'shipping': SHIPPING,
        'total_price_with_shipping': total_price + SHIPPING
    }
    
    return render(request, 'cart/display.html', context=context)

def payment_page(request, cart_id):
    SHIPPING = 10
    user_cart = Cart.objects.get(id=cart_id)
    cart_items = CartItem.objects.filter(cart=user_cart)
    amount = 0
    currency = user_cart.currency

    for cart_item in cart_items:
        product = Product.objects.get(pk=cart_item.product_id)
        amount += (cart_item.amount * product.price)

    dotpay_id = '742805'  # TODO hide in cofngi
    amount = str(round(amount + SHIPPING, 2))
    description = 'Test'
    type = '0'
    url = f'http://340b-87-239-222-251.ngrok.io{reverse("cart:thanks_page")}'
    urlc = 'http://340b-87-239-222-251.ngrok.io/cart/response'
    payment_data = {
        'id': dotpay_id,
        'amount': amount,
        'currency': currency,
        'description': description,
        'type': type,
        'url': url,
        'urlc': urlc
    }
    test_env = 'https://ssl.dotpay.pl/test_payment/'
    chk = create_payment_chk(payment_data)
    
    payment_url = f'{test_env}?id={dotpay_id}&amount={amount}&currency={currency}&description={description}&type={type}&url={url}&urlc={urlc}&chk={chk}'
    request.session['card_id'] = cart_id

    return redirect(payment_url)


def delete_cart_item_page(request, cart_item_id):
    pass

@csrf_exempt
def display_thanks_page(request):
    status = request.GET.get('status', 'none')
    
    context = {
        'status': status
    }

    return render(request, 'cart/thanks_page.html', context=context)


@csrf_exempt
def display_payment_respone_page(request):
    print(request.POST)
    print(f'Get response from payment in urlc, status: {request.POST["operation_status"]}')

    if request.POST['operation_status'] == 'completed':
        email = request.POST['email']
        amount = request.POST['operation_original_amount']
        card_id = request.POST['operation_number']
        send_bill_email(email, card_id, amount)

    return HttpResponse('OK')

def display_checkout_page(request):
    return render(request, 'cart/checkout.html', context={})