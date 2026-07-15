from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Category, Product, Comment
from shop.forms import CommentModelForm, OrderModelForm, ProductForm
from django.db.models import Q, Avg, Value, FloatField 
from django.contrib import messages
from django.db.models.functions import Coalesce


def shop(request, category_id : int | None = None):
    categories = Category.objects.all()
    products = Product.objects.all()
    filter_type = request.GET.get('filter_type', '')
    search_query = request.GET.get('q', '')
    products = Product.objects.annotate(avg_comment = Coalesce(Avg('comments__rating') , Value(0), output_field=FloatField()))
    form = ProductForm()
    
    if category_id is not None:
        products = products.filter(category = category_id)
    
    if search_query:
        products = products.filter(Q(name__icontains=search_query))

    if filter_type == 'expensive':
        products = products.order_by('-price')
    elif filter_type == 'cheap':
        products = products.order_by('price')
    else:
        products = products.order_by('-avg_comment')

    
    context = {
        'categories':categories,
        'products': products,
        'form': form
    }
    return render(request, 'shop/home.html', context)


def detail(request, product_id):
    comments = Comment.objects.filter(product=product_id).order_by('-created_at')
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    form = ProductForm(instance=product)
    
    
    context = {
        'product':product,
        'comments':comments,
        'related_products':related_products,
        'form': form
    }
    return render(request, 'shop/detail.html', context)


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


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('home')
    return redirect('home')


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    context = {
        'product': product,
        'form': form
    }

    return render(request, 'shop/detail.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('home',)
    return redirect('detail', product_id=product.id)