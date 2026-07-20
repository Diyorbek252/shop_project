from django.shortcuts import render, redirect
from users.forms import LoginForm, RegistorForm
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib import messages
# Create your views here.

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login_auth(request, user)
                return redirect('shop:home')
            else:
                messages.error(request, 'Username yoki parol noto\'g\'ri')
    else:
        form = LoginForm()
    return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = RegistorForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login_auth(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz")
            return redirect('shop:home')
        else:
            messages.error(request, "Formani to'ldirishda xatolik bor")
    else:
        form = RegistorForm()

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)

def logout(request):
    logout_auth(request)
    messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz')
    return redirect('shop:home')