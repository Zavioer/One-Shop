from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .forms import CustomUserCreationForm


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class ViewsUserTestCase(TestCase):
    def test_01__register_view_render_correct(self):
        response = self.client.get(reverse('account:register'))

        self.assertEqual(response.status_code, 200)

    def test_02__check_if_register_form_is_valid(self):
        form = CustomUserCreationForm(data={
            'email': 'user@b.com',
            'password1': 'A1s2d3f4%',
            'password2': 'A1s2d3f4%'
        })

        self.assertTrue(form.is_valid())

    def test_03__check_if_register_view_correct_add_user(self):
        response = self.client.post(
            reverse('account:register'), {
            'email': 'user@b.com',
            'password1': 'A1s2d3f4%',
            'password2': 'A1s2d3f4%'
        })

        self.assertEqual(response.status_code, 200)
        print('Test 3a: Correct created new user.')
        
        self.assertTemplateUsed(response, 'account/email_confirm.html')
        print('Test 3b: Correct render template after user creation.')

    def test_04__check_user_login(self):
        User = get_user_model()
        User.objects.create_user(email='normal@user.com', password='foo')

        user_login = self.client.login(email='normal@user.com', password='foo')
        self.assertTrue(user_login)
        print('Test 4: User can correctly login.')

