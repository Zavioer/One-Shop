from django.urls import path
from .views import (
    all_products_page,
    add_product_page,
    detail_product_page,
    delete_product_page,
    update_product_page,
    add_category_page,
    delete_category_page,
    update_category_page,
    add_comment_to_product,
    add_comment_rate
)


app_name = 'product'
urlpatterns = [
    path('', all_products_page, name='home'),
    path('add', add_product_page, name='add'),
    path('details/<pk>', detail_product_page, name='details'),
    path('delete/<pk>', delete_product_page, name='delete'),
    path('update/<pk>', update_product_page, name='update'),
    path('category/add', add_category_page, name='add-category'),
    path('category/delete/<pk>', delete_category_page, name='delete-category'),
    path('category/update/<pk>', update_category_page, name='update-category'),
    path('comment/add/<product_pk>', add_comment_to_product, name='add-comment'),
    path('comment/<comment_pk>/add/rate/<product_id>', add_comment_rate, name='add-comment-rate')
]
