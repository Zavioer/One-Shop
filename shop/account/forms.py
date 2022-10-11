from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, required=True)
    email.widget.attrs.update({'class': 'form-control'})
    password1 = forms.CharField(max_length=60, widget=forms.PasswordInput)
    password1.widget.attrs.update({'class': 'form-control'})
    password2 = forms.CharField(max_length=60, widget=forms.PasswordInput)
    password2.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=60, required=True)
    email.widget.attrs.update({'class': 'form-control'})
    password = forms.CharField(max_length=60, widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'form-control'})


class RegisterForm(forms.Form):
    pass
