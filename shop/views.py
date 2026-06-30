from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product, Comment
# Create your views here.

def shop(request, category_id : int | None = None):
    categories = Category.objects.all()
    products = Product.objects.all()
    
    if category_id is not None:
        products = Product.objects.filter(category = category_id)
    
    context = {
        'categories':categories,
        'products': products
    }
    return render(request, 'shop/home.html', context)


def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product':product
    }
    return render(request, 'shop/detail.html', context)