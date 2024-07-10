from pyexpat.errors import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import loader
from .models import CartItem, Category, Product, Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import pandas as pd
import sqlite3
#Trang đăng kí
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Kiểm tra xem tài khoản đã tồn tại hay chưa
        if User.objects.filter(username=username).exists():
            error_message = "Tên đăng nhập đã tồn tại. Vui lòng chọn tên đăng nhập khác."
            return render(request, 'register.html', {'error_message': error_message})

        # Kiểm tra mật khẩu và xác nhận mật khẩu có khớp nhau hay không
        if password != confirm_password:
            error_message = "Mật khẩu và xác nhận mật khẩu không khớp."
            return render(request, 'register.html', {'error_message': error_message})

        # Tạo tài khoản mới
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Xác thực tài khoản và chuyển hướng trang
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')

    return render(request, 'register.html')
# Trang đăng nhập
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')  # Chuyển hướng đến product-list
        else:
            error_message = "Tên đăng nhập hoặc mật khẩu không chính xác. "
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('customer')

def view_home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'view_home.html', context)

def products_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products_by_category.html', context)
# Xem danh sách sản phẩm
def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'product_list.html', context)

#Thêm sản phầm vào giỏ hàng
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    quantity = int(request.POST['quantity'])

    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart',)
#Xóa sản phẩm khỏi giỏ hàng    
@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(customer=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')
#Xem chi tiết giỏ hàng

@login_required
def cart(request):
    cart = Cart.objects.get(customer=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = 0
    total_quantity = 0

    for item in cart_items:
        item.total_price = item.get_total_price()  
        total_price += item.product.price * item.quantity
        total_quantity += item.quantity

    formatted_total_price = '{:,.0f}'.format(total_price).replace(',', '.')  

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': formatted_total_price,  
        'total_quantity': total_quantity
    }
    return render(request, 'cart.html', context)
#Xem thông tin tóm tắt (tổng tiền, số mặt hàng) của giỏ hàng
@login_required
def cart_summary(request):
    cart = Cart.objects.get(customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    
    context = {
        'total_price': total_price,
        'total_quantity': total_quantity,
    }
    
    return render(request, 'cart_summary.html', context)
#Xem chi tiết sản phẩm
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'product_detail.html', context)
#Xem danh sách các sản phẩm mới cập nhật(10 sản phẩm)
def new_products(request):
    new_products = Product.objects.order_by('-id')[:10]  
    return render(request, 'new_products.html', {'new_products': new_products})

#Tìm kiếm sản phẩm nâng cao (dựa vào khoảng giá và nhà cung cấp)
def search_products_price_supplier(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    supplier = request.GET.get('supplier')

    # Truy xuất dữ liệu từ cơ sở dữ liệu dựa trên các tiêu chí tìm kiếm
    products = Product.objects.filter(price__range=(min_price, max_price), supplier=supplier)

    context = {
        'products': products,
        'min_price': min_price,
        'max_price': max_price,
        'supplier': supplier
    }

    return render(request, 'search_products_price_supplier.html', context)
#Tìm kiếm sản phẩm theo tên 
def search_product_name(request):
    query = request.GET.get('search_query')
    products = Product.objects.filter(name__icontains=query)

    if not query:
        # Nếu không có nhập liệu, hiển thị thông báo không có sản phẩm khớp
        message = "Không có sản phẩm nào khớp với yêu cầu tìm kiếm."
        return render(request, 'search.html', {'message': message})
    
    context = {
        'query': query,
        'products': products
    }

    return render(request, 'search.html', context)


