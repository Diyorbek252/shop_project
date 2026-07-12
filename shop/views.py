from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Category, Product, Comment
from shop.forms import CommentModelForm, OrderModelForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib import messages


def shop(request, category_id : int | None = None):
    categories = Category.objects.all()
    products = Product.objects.all()
    filter_type = request.GET.get('filter_type', '')
    search_query = request.GET.get('q', '')
    
    if category_id is not None:
        products = products.filter(category = category_id)
    
    if search_query:
        products = products.filter(Q(name__icontains=search_query))

    if filter_type == 'expensive':
        products = products.order_by('-price')
    elif filter_type == 'cheap':
        products = products.order_by('price')

    
    context = {
        'categories':categories,
        'products': products
    }
    return render(request, 'shop/home.html', context)


def detail(request, product_id):
    comments = Comment.objects.all().order_by('-created_at')
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    
    
    context = {
        'product':product,
        'comments':comments,
        'related_products':related_products
    }
    return render(request, 'shop/detail.html', context)


# def add_comment(request, pk):
#     product = get_object_or_404(Product, id = pk)
#     name = request.POST.get('name', '')
#     email = request.POST.get('email', '')
#     message = request.POST.get('message', '')
#     image = request.FILES.get('image', '')
#     rating = request.POST.get('rating', '')
#     comment = Comment(name=name, email=email, message=message, file=image, rating=rating)
#     comment.product = product
#     comment.save()

#     return redirect('detail', pk)


def add_comment(request, pk):
    product = get_object_or_404(Product, id = pk)
    if request.method == 'POST':
        form = CommentModelForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('detail', pk)
        else:
            form = CommentModelForm()

    context = {
        'form':form
    }

    return render(request, 'shop/detail.html', context)


def order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = OrderModelForm()
    
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.stock < order.quantity:
                messages.add_message(
                    request,
                    messages.WARNING,
                    f'Omborda mahsulotlar yetarli emas. Qolgani {product.stock}'
                )
            else:
                product.stock -= order.quantity
                product.save()
                order.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Buyurtma muvaffaqiyatli amalga oshirildi'
                )
        return redirect('detail', product_id=pk)       
    context = {
        'product':product,
        'form':form

    }
    return render(request, 'shop/detail.html', context)
