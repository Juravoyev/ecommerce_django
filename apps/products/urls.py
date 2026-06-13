from django.urls import path

from .views import category_detail, category_list, product_list


urlpatterns = [
    path('', product_list, name='product_list'),
    path('categories/', category_list, name='category_list'),
    path('categories/<int:pk>/', category_detail, name='category_detail'),
]
