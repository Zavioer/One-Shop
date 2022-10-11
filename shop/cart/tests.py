import email
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from product.models import Category, Product
from .models import Cart, CartItem


# Create your tests here.
class CartTestCase(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='testcat')
        
        name = 'Test Product'
        description = 'Test description for product'
        price = 123.123
        category = self.category

        self.product = Product.objects.create(
            name=name, description=description, price=price, category=category)

        User = get_user_model()
        self.user = User.objects.create_user(email='normal@user.com', password='foo')
        
        self.cart = Cart.objects.create(user=self.user)
        self.client.login(email='normal@user.com', password='foo')

    def test_01__check_if_item_add_to_cart_view(self):
        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}), 
            {'user': self.user})

        self.assertRedirects(response, reverse('product:home'))

        cart_item = CartItem.objects.get(cart_id=self.cart.id, product_id=self.product.id)

        self.assertEqual(cart_item.product_id, self.product.id)
        print('Test 1a: Add to cart view is correct.')

        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}), 
            {'user': self.user})

        self.assertRedirects(response, reverse('product:home'))
        cart_item = CartItem.objects.get(cart_id=self.cart.id, product_id=self.product.id)
        self.assertEqual(cart_item.amount, 2)
        print('Test 1b: Increase on add to cart is correct.')

