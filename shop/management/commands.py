import csv
import os

import django
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maya_pharm.settings")
django.setup()

from shop.models import Category, Brand, Product, Order, OrderItem


def import_categories(file_path):
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Category.objects.create(
                id=row["id"],
                name=row["name"],
                parent_id=row["parent"] if row["parent"] else None,
                slug=row["slug"],
            )


def import_brands(file_path):
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Brand.objects.create(id=row["id"], name=row["name"], slug=row["slug"])


def import_products(file_path):
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Product.objects.create(
                id=row["id"],
                status=row["status"],
                brand_id=row["brand"] if row["brand"] else None,
                thumbnail=row["thumbnail"],
                title=row["title"],
                sale_price=row["sale_price"],
                short_desc=row["short_desc"],
                long_desc=row["long_desc"],
                slug=row["slug"],
            )


def import_orders(file_path):
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Order.objects.create(
                id=row["id"],
                status=row["status"],
                subtotal_price=row["subtotal_price"],
                total_price=row["total_price"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                shipping_address=row["shipping_address"],
                city=row["city"],
                phone_number=row["phone_number"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )


def import_order_items(file_path):
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            OrderItem.objects.create(
                id=row["id"],
                order_id=row["order"],
                product_id=row["product"],
                price=row["price"],
                quantity=row["quantity"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )


def re_process_images():
    for product in Product.objects.all():
        if product.thumbnail:
            with open(product.thumbnail.path, "rb") as f:
                content = f.read()

            # Save the content back to the same field to trigger re-processing
            product.thumbnail.save(
                product.thumbnail.name, ContentFile(content), save=False
            )
            product.save()


if __name__ == "__main__":
    import_categories("/home/thefrisb/Desktop/django/maya_pharm/exports/categories.csv")
    import_brands("/home/thefrisb/Desktop/django/maya_pharm/exports/brands.csv")
    import_products("/home/thefrisb/Desktop/django/maya_pharm/exports/products.csv")
