from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Product(models.Model):
    HIDDEN = "PRIVATE"
    ACTIVE = "ACTIVE"
    STATUS_CHOICES = [
        (HIDDEN, "Private"),
        (ACTIVE, "Published")
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=HIDDEN
    )
    title = models.CharField(max_length=256)
    sale_price = models.IntegerField()

    def __str__(self):
        return f'{self.title}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('Processing', 'Processing'),
        ('Paid', 'Paid'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    subtotal_price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_order_total(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_item_count(self):
        return self.items.count()

    def createOrderItems(self, cartItems):
        subtotal = 0
        for item in cartItems:
            OrderItem.objects.create(order=self, product=item.product, price=item.price, quantity=item.quantity)
            subtotal += item.get_total_price()
        return subtotal

    def setSubtotalPrice(self, subtotal):
        self.subtotal_price = subtotal

    def setTotalPrice(self, total):
        self.total_price = total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return self.price * self.quantity

    def as_dict(self):
        return {
            'product': self.product.id,
            'price': str(self.price),
            'quantity': self.quantity,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
