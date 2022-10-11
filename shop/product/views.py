from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import redirect, render, get_object_or_404
from django.urls.base import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Comment, Product, Category, CommentRate, VoteType
from .forms import CategoryForm, ProductForm, CommentForm


# Product
def all_products_page(request):
    products = Product.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(products, per_page=12)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    context = {
        'products': page_obj,
        'categories': categories,
    }
    
    return render(request, 'product/home.html', context)

def add_product_page(request): 
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request, 'product/add.html', {})
        else:
            return render(request, 'product/add.html', {})
    else:
        form = ProductForm()
        context = {
            'form': form
        }

        return render(request, 'product/add.html', context)


def detail_product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments_query = Comment.objects.filter(product_id=pk)
    user_comment = Comment.objects.filter(user_id=request.user.id, product_id=pk)

    comments = comments_query if comments_query else []
    # can_comment = False if comments else True
    can_comment =  True
    comment_form = CommentForm

    context = {
        'product': product,
        'comments': comments,
        'can_comment': can_comment,
        'form': comment_form
    }

    return render(request, 'product/details.html', context)


def delete_product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)

    product.delete()

    return redirect('product:home')

def update_product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        updated_product = ProductForm(request.POST or None, instance=product)

        if updated_product.is_valid():
            updated_product.save(commit=False)
            product.save()

            return redirect('product:home')
        else:
            return HttpResponse(updated_product.errors)
    else:
        form = ProductForm(request.POST or None, instance=product)
        context = {
            'form': form
        }

    return render(request, 'product/update.html', context)

def add_category_page(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('product:home')
        else:
            return render(request, 'category/add.html', {})
    else:
        form = CategoryForm()
        context = {
            'form': form
        }

        return render(request, 'category/add.html', context)


def delete_category_page(request, pk):
    category = get_object_or_404(Category, pk=pk)

    category.delete()
    
    return redirect('product:home')

def update_category_page(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        updated_category = CategoryForm(request.POST or None, instance=category)

        if updated_category.is_valid():
            updated_category.save(commit=False)
            category.save()

            return redirect('product:home')
        else:
            return redirect('product:home')
    else:
        form = CategoryForm(request.POST or None, instance=category)
        context = {
            'form': form
        }

        return render(request, 'category/update.html', context)


def add_comment_to_product(request, product_pk):
    # TODO use form and add values before insert
    if request.method == 'POST':
        new_comment = Comment()
        new_comment.body = request.POST['body']
        new_comment.user_id = request.user.id
        new_comment.product_id = product_pk

        new_comment.save()

        response = {
            'add_comment': True
        }
        
        return JsonResponse(response)
    else:
        return HttpResponse('Not POST request')


def add_comment_rate(request, product_pk, comment_pk):
    if request.method == 'POST':
        vote = request.POST['vote']
        new_comment_rate = CommentRate()
        new_comment_rate.user_id = request.user.id
        new_comment_rate.product_id = product_pk
        new_comment_rate.vote = vote

        new_comment_rate.save()

        # change comment value
        comment = Comment.objects.get(pk=comment_pk)

        if vote == VoteType.plus:
            comment.vote_plus += 1
        elif vote == VoteType.minus and comment.vote_minus >= 0:
            comment.vote_minus -= 1
        else:
            return JsonResponse({
                'add_rate': False,
                'message': 'Invalid vote type!'
            })

        comment.save()

        response = {
            'add_rate': True,
            'message': 'Rate added correctly.',
            'vote_plus': comment.vote_plus,
            'vote_minus': comment.vote_minus
        }

        return JsonResponse(response)
    else:
        return HttpResponse('Not POST request!')
        