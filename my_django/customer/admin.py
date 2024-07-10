from django.contrib import admin
from django.http import HttpResponse
from .models import Cart, Category, Product,CartItem
import pandas as pd


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','category', 'name', 'formatted_price','supplier')
    search_fields = ('name','price','id')  
    actions = ['export_to_excel']
    
    def formatted_price(self, obj):
        return obj.formatted_price()  

    formatted_price.short_description = 'Price'

    def export_to_excel(self, request, queryset):
        # Truy vấn dữ liệu từ cơ sở dữ liệu
        data = queryset.values()

        # Chuyển đổi dữ liệu thành DataFrame
        df = pd.DataFrame.from_records(data)

        # Tạo một phản hồi HTTP để xuất tệp Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Book1.xlsx"'

        # Xuất dữ liệu DataFrame sang tệp Excel
        df.to_excel(response, index=False)

        return response


admin.site.register(Product, ProductAdmin)
