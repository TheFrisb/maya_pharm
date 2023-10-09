from django.db import models


# Create your models here.
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_product(self, product, quantity=1):
        cart_item = CartItem.objects.filter(cart=self, product=product).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=self,
                product=product,
                price=product.sale_price,
                quantity=quantity
            )
        return cart_item

    def update_product(self, product, quantity):
        cart_item = CartItem.objects.filter(cart=self, product=product).first()
        if not cart_item:
            return False
        if quantity < 1:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        return True

    def remove_product(self, product):
        CartItem.objects.filter(cart=self, product=product).delete()

    def get_cart_total(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_count_and_total(self):
        total_price = 0
        product_count = 0
        for item in self.items.all():
            total_price += item.get_total_price()
            product_count += 1
        return total_price, product_count

    def as_dict(self):
        total_price, product_count = self.get_count_and_total()

        return {
            'total_price': total_price,
            'productCount': product_count
        }


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return self.price * self.quantity

    def as_dict(self):
        prod = self.product
        return {
            'product_id': prod.pk,
            'product_title': prod.title,
            'product_thumbnail': prod.thumbnail.url,
            'quantity': self.quantity,
            'price': self.price,
            'price_total': self.get_total_price(),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


    def __str__(self):
        return f'{self.product.title} x {self.quantity} | price: {self.price}'
