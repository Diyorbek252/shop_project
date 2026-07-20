from django.urls import path
from shop.views import shop, detail, add_comment, order, add_product, edit_product, delete_product

app_name = 'shop'

urlpatterns = [
    path('home/', shop, name='home'),
    path('category/<int:category_id>/products/',shop ,name='products_of_category'),
    path('detail/<int:product_id>', detail, name='detail'),
    path('add_comment/<int:pk>', add_comment, name='add_comment'),
    path('order/<int:pk>', order, name='order'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:product_id>', edit_product, name='edit_product'),
    path('delete_product<int:product_id>', delete_product, name='delete_product')
]