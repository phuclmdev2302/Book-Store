from django.urls import path
from . import views

urlpatterns = [

    path('', views.view_home, name='customer'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register),
    path('login/',    views.login_view, name = 'login' ),

    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product-list/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),
    path('cart-summary/', views.cart_summary, name='cart_summary'),

    path('product-detail/<int:product_id>', views.product_detail, name ='product_detail' ),

    path('new-products/', views.new_products, name='new_products'),
    path('search-product-name/', views.search_product_name, name='search_product_name'),
    path('search-products-price-supplier/', views.search_products_price_supplier, name='search_products_price_supplier'),
    path('logout/', views.logout, name='logout'),
    path('products-by-category/<int:category_id>/', views.products_by_category, name='products_by_category'),    ]