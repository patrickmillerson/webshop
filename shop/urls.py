from django.urls import path
from .views import (
    register,
    login_view,
    request_to_buy,
    product_list,
    add_product,
    profile_view,
    edit_profile,
    delete_product,
    delete_account,
    ProductDetailView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('account/delete/', delete_account, name='delete_account'),
    path('', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),
    path('products/request_to_buy/<int:product_id>/', request_to_buy, name='request_to_buy'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('products/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('logout/', LogoutView.as_view(next_page='product_list'), name='logout'),  # Redirect to product list after logout
]
