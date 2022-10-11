from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.display_panel_page, name='panel'),
    path('product', views.product_panel_page, name='panel-product'),
    path('category', views.category_panel_page, name='panel-category'),
]