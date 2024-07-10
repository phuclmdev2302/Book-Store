from django.db import models
from django.contrib.auth.models import User
import pandas as pd
import sqlite3
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)  # Thêm thuộc tính 'quantity'
    profile_picture = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name
    
    def formatted_price(self):
        return '{:,.0f}'.format(self.price).replace(',', '.')
    
class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product) 

    def get_total_price(self):
        total_price = sum(product.price for product in self.products.all())
        formatted_total_price = '{:,.0f}'.format(total_price).replace(',', '.')
        return formatted_total_price
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=0)

    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price

    def formatted_total_price(self):
        total_price = self.get_total_price()
        formatted_price = '{:,.0f}'.format(total_price).replace(',', '.')
        return formatted_price

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
# class Order(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product) 
#     date_created = models.DateTimeField(auto_now_add=True)
#     is_completed = models.BooleanField(default=False)

# class Feedback(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE) 
#     content = models.TextField()
#     rating = models.PositiveIntegerField()

# class CustomerAccount(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=200)
#     phone = models.CharField(max_length=20)

#     def __str__(self):
#         return self.user.username