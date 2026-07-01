from django.forms import ModelForm, Form
from shop.models import Comment, Order

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