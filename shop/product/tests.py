from cmath import pi
from django.test import TestCase
from django.urls import reverse
from .models import Category, Product
from .forms import ProductForm


# Create your tests here.
class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='testcat')
        
        name = 'Test Product'
        description = 'Test description for product'
        price = 123.123
        category = self.category

        self.product = Product.objects.create(
            name=name, description=description, price=price, category=category)
        
    def test_01__check_if_cattegory_added_correctly(self):
        name = 'fruits'

        category = Category.objects.create(name=name)
        category.save()

        self.assertEqual(category.name, name)
        print('Test 1: Category correct add by model.')

    def test_02__check_add_view(self):
        # valid form 
        data = {
                'name': 'Test Product',
                'description': 'Test desc',
                'price': 123.23,
                'category': self.category.id
            }
        form = ProductForm(data=data)
        self.assertTrue(form.is_valid())
        print(form.errors)
        

        prod_cnt = Product.objects.count()

        response = self.client.post(
            reverse('product:add'), data)

        prod_cnt_after = Product.objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(prod_cnt_after, prod_cnt + 1)
        print('Test 2: Product add view correct.')

    def test_03__check_product_del_view(self):
        prod_cnt = Product.objects.count()
        response = self.client.get(reverse('product:delete', kwargs={'pk': self.product.id}))
        prod_cnt_after = Product.objects.count()

        # Why code 302 ??
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(prod_cnt_after, prod_cnt - 1)

    def test_04__check_product_update_view(self):
        p_name = self.product.name
        p_price = self.product.price

        response = self.client.post(
            reverse('product:update', kwargs={'pk': self.product.id}),{
                'name': 'czosnek', 
                'price': 45, 
                'description': self.product.description,
                'category': self.category.id
                })

        p_new = Product.objects.get(id=self.product.id)
        print(response.content)
        self.assertRedirects(response, reverse('product:home'))

        self.assertNotEqual(p_name, p_new.name)
        self.assertNotEqual(p_price, p_new.price)

        self.assertEqual(p_new.name, 'czosnek')
        print('Test 4: Update poduct view correct.')


