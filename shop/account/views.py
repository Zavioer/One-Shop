import hashlib
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, LoginForm, RegisterForm
from .models import CustomUser
from .google_auth import oauth


def register_page(request):
    form = CustomUserCreationForm
    context = {
        'form': form
    }
        
    if request.method == 'POST':        
        form = CustomUserCreationForm(request.POST)
        password_hash = None

        if form.is_valid():
            user = form.save()
            password_hash = hashlib.md5(user.email.encode()) 
            hext_hash = password_hash.hexdigest()
            user.email_hash = hext_hash
            user.save()
            
            # mail confirm
            subject = 'SHOP - Confirm account'
            confirm_url = reverse('account:confirm_email', \
                kwargs={'email': user.email, 'hash': hext_hash})
            email_body = f'Configrm your message here: http:/127.0.0.1:8000{confirm_url}'

            send_mail(
                subject,
                email_body,
                'shop-norepl@shop.com',
                [request.POST.get('email')],
                fail_silently=False
            )

            messages.success(request, 'You account created correctly!')
            return render(request, 'account/email_confirm.html', context={})
        else:
            for error in form.errors:
                messages.error(request, error)

    return render(request, 'account/register.html', context)

def login_page(request):
    form = LoginForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

            email = request.POST.get('email')
            password = request.POST.get('password')
            user = CustomUser.objects.get(email=email)

            if user.check_password(password):
                login(request, user)

                return redirect('product:home')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            return HttpResponse('Please enable cookes and try again.')

    request.session.set_test_cookie()
    return render(request, 'account/login.html', context)

@login_required
def logout_page(request):
    logout(request)

    return redirect('product:home')

def confirm_email_page(request, email, hash):
    user = CustomUser.objects.get(email=email)

    if user.email_hash == hash and user.is_active == False:
        user.is_active = True
        user.save()
        messages.info(request, 'Account correctly activated.')

        return redirect('product:home')

    return HttpResponse('Account activated eariler')

def login_oauth_page(request):
    google = oauth.create_client('google')
    redirect_uri = request.build_absolute_uri(reverse('account:auth'))

    return google.authorize_redirect(request, redirect_uri)


def auth_page(request):
    token = oauth.google.authorize_access_token(request)
    user = oauth.google.parse_id_token(request, token)
    request.session['user'] = user

    return redirect('account:login-oauth-user')

def login_oauth_user_page(request):
    user = request.session['user']

    try:
        user_local = CustomUser.objects.get(email=user['email'])
        login(request, user_local)
    except CustomUser.DoesNotExist:
        new_user = CustomUser.objects.create(email=user['email'], activated=user['email_verified'])
        new_user.save()
        login(request, new_user)
     
    return redirect('product:home')

def display_account_page(request): 
    return render(request, 'account/account.html', context={})