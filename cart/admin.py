from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.


@admin.register(Cart)
class ModelNameAdmin(admin.ModelAdmin):
    pass

admin.site.register(CartItem)
