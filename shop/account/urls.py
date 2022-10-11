from django.urls import path
from .views import (
    register_page,
    login_page,
    logout_page,
    confirm_email_page,
    login_oauth_page,
    auth_page,
    login_oauth_user_page,
    display_account_page)


app_name = 'account'
urlpatterns = [
    path('register', register_page, name='register'),
    path('login', login_page, name='login'),
    path('logout', logout_page, name='logout'),
    path('confirm/email/<email>/hash/<hash>', confirm_email_page, name='confirm_email'),
    path('login/auth', login_oauth_page, name='login-auth'),
    path('login/auth/o', auth_page, name='auth'),
    path('login/auth/user', login_oauth_user_page, name='login-oauth-user'),
    path('account', display_account_page, name='account'),
]
