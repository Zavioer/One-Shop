from django.shortcuts import render
from .models import VwMostSoldProduct

from product.models import Product, Category

from plotly.offline import plot
from plotly.graph_objects import Bar


# Create your views here.
def display_panel_page(request):
    objects = VwMostSoldProduct.objects.all().values()
    limited = objects[:10]
    x = []
    y = []

    for obj in limited:
        x.append(obj['name'])
        y.append(obj['amount'])

    chart = plot([Bar(x=x, y=y,
                    name='test')],
            output_type='div')

    context = {
        'objects': objects,
        'chart': chart
    }
    return render(request, 'dashboard/panel.html', context)


def product_panel_page(request):
    products = Product.objects.all().order_by('id')

    context = {
        'products': products
    }
    return render(request, 'dashboard/product_panel.html', context)


def category_panel_page(request):
    categories = Category.objects.all().order_by('id')

    context = {
        'categories': categories
    }
    return render(request, 'dashboard/category_panel.html', context)
