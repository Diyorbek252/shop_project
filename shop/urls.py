from django.urls import path
from shop.views import shop, detail

urlpatterns = [
    path('home/', shop, name='home'),
    path('category/<int:category_id>/products/',shop ,name='products_of_category'),
    path('detail/<int:product_id>', detail, name='detail')
]