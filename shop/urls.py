from django.urls import path
from shop.views import shop, detail, add_comment, order

urlpatterns = [
    path('home/', shop, name='home'),
    path('category/<int:category_id>/products/',shop ,name='products_of_category'),
    path('detail/<int:product_id>', detail, name='detail'),
    path('add_comment/<int:pk>', add_comment, name='add_comment'),
    path('order/<int:pk>', order, name='order')
]