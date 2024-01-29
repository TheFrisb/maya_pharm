from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField
from transliterate import translit


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Име")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Припаѓа на",
                               related_name='subcategories')
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            latin_name = translit(self.name, 'mk', reversed=True)
            slug_candidate = slugify(latin_name)
            unique_slug = slug_candidate
            num = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug_candidate, num)
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_page', kwargs={'slug': self.slug})

    def __str__(self):
        if self.parent is None:
            return self.name
        return f"[{self.parent}] {self.name}"

    class Meta():
        verbose_name = "Категорија"
        verbose_name_plural = "Категории"


class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name="Име")
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            latin_name = translit(self.name, 'mk', reversed=True)
            slug_candidate = slugify(latin_name)
            unique_slug = slug_candidate
            num = 1
            while Brand.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug_candidate, num)
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = "Бренд"
        verbose_name_plural = "Брендови"

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

    categories = models.ManyToManyField(Category, related_name='products', verbose_name='Категории')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', verbose_name="Бренд", blank=True, null=True)
    thumbnail = ProcessedImageField(upload_to="products/%Y/%m/%d/", verbose_name="Слика", blank=True, null=True)
    title = models.CharField(max_length=256)
    sale_price = models.IntegerField(verbose_name="Цена")
    short_desc = RichTextField(verbose_name="Краток опис", blank=True, null=True)
    long_desc = RichTextField(verbose_name="Долг опис", blank=True, null=True)
    slug = models.SlugField(blank=True, max_length=350)

    def save(self, *args, **kwargs):
        if not self.slug:
            latin_name = translit(self.title, 'mk', reversed=True)
            slug_candidate = slugify(latin_name)
            unique_slug = slug_candidate
            num = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug_candidate, num)
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('shop:product_page', kwargs={'name': self.slug})

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Processing'),
        ('confirmed', 'Confirmed'),
        ('deleted', 'Deleted')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    subtotal_price = models.IntegerField(default=0, verbose_name="Цена без достава")
    total_price = models.IntegerField(default=0, verbose_name="Вкупна цена")
    first_name = models.CharField(max_length=50, verbose_name="Име")
    last_name = models.CharField(max_length=50, verbose_name="Презиме")
    shipping_address = models.CharField(max_length=255, verbose_name="Адреса")
    city = models.CharField(max_length=255, default="Strumica", verbose_name="Град")
    phone_number = models.CharField(max_length=15, verbose_name="Телефонски број")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Креиран во")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Модифициран во")

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

    def getFullName(self):
        return f'{self.first_name} {self.last_name}'

    def set_to_confirm(self):
        self.status = 'confirmed'
        self.save()

    def set_to_deleted(self):
        self.status = 'deleted'
        self.save()

    def set_to_pending(self):
        self.status = 'pending'
        self.save()

    class Meta:
        verbose_name = "Порачка"
        verbose_name_plural = "Порачки"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Порачка")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    price = models.IntegerField(verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количина")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Креиран во")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Модифициран во")

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

    def details(self):
        return f'{self.product.title} - 4 x {self.price} ден'

    def __str__(self):
        return f'{self.product.title} x {self.quantity}'

    class Meta:
        verbose_name = "Порачен продукт"
        verbose_name_plural = "Порачени продукти"
