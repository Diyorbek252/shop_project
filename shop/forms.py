from django.forms import ModelForm, Form
from django import forms
from shop.models import Comment, Order, Product

class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        # fields = ['id', 'name', 'email', 'message', 'created']
        # fields = '__all__'
        exclude = ('id', 'product')

class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('id', 'product')
        


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'discount', 'image']  # o'zingizning model maydonlaringizga moslang
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }