import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from shop.models import Category, Brand, Product, Order, OrderItem


class Command(BaseCommand):
    help = "Export models to CSV files"

    def handle(self, *args, **options):
        base_media_url = "https://www.majafarm.mk/media/"
        output_dir = os.path.join(settings.BASE_DIR, "exports")
        os.makedirs(output_dir, exist_ok=True)

        self.export_categories(output_dir)
        self.export_brands(output_dir)
        self.export_products(output_dir, base_media_url)
        self.export_orders(output_dir)
        self.export_order_items(output_dir)

    def export_categories(self, output_dir):
        categories = Category.objects.all()
        with open(
            os.path.join(output_dir, "categories.csv"),
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            fieldnames = ["id", "name", "parent", "slug"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for category in categories:
                writer.writerow(
                    {
                        "id": category.id,
                        "name": category.name,
                        "parent": category.parent.id if category.parent else "",
                        "slug": category.slug,
                    }
                )

    def export_brands(self, output_dir):
        brands = Brand.objects.all()
        with open(
            os.path.join(output_dir, "brands.csv"), "w", newline="", encoding="utf-8"
        ) as csvfile:
            fieldnames = ["id", "name", "slug"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for brand in brands:
                writer.writerow(
                    {"id": brand.id, "name": brand.name, "slug": brand.slug}
                )

    def export_products(self, output_dir, base_media_url):
        products = Product.objects.all()
        with open(
            os.path.join(output_dir, "products.csv"), "w", newline="", encoding="utf-8"
        ) as csvfile:
            fieldnames = [
                "id",
                "status",
                "brand",
                "thumbnail",
                "title",
                "sale_price",
                "short_desc",
                "long_desc",
                "slug",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                writer.writerow(
                    {
                        "id": product.id,
                        "status": product.status,
                        "brand": product.brand.id if product.brand else "",
                        "thumbnail": (
                            base_media_url + product.thumbnail.name
                            if product.thumbnail
                            else ""
                        ),
                        "title": product.title,
                        "sale_price": product.sale_price,
                        "short_desc": product.short_desc,
                        "long_desc": product.long_desc,
                        "slug": product.slug,
                    }
                )

    def export_orders(self, output_dir):
        orders = Order.objects.all()
        with open(
            os.path.join(output_dir, "orders.csv"), "w", newline="", encoding="utf-8"
        ) as csvfile:
            fieldnames = [
                "id",
                "status",
                "subtotal_price",
                "total_price",
                "first_name",
                "last_name",
                "shipping_address",
                "city",
                "phone_number",
                "created_at",
                "updated_at",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for order in orders:
                writer.writerow(
                    {
                        "id": order.id,
                        "status": order.status,
                        "subtotal_price": order.subtotal_price,
                        "total_price": order.total_price,
                        "first_name": order.first_name,
                        "last_name": order.last_name,
                        "shipping_address": order.shipping_address,
                        "city": order.city,
                        "phone_number": order.phone_number,
                        "created_at": order.created_at,
                        "updated_at": order.updated_at,
                    }
                )

    def export_order_items(self, output_dir):
        order_items = OrderItem.objects.all()
        with open(
            os.path.join(output_dir, "order_items.csv"),
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:
            fieldnames = [
                "id",
                "order",
                "product",
                "price",
                "quantity",
                "created_at",
                "updated_at",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in order_items:
                writer.writerow(
                    {
                        "id": item.id,
                        "order": item.order.id,
                        "product": item.product.id,
                        "price": item.price,
                        "quantity": item.quantity,
                        "created_at": item.created_at,
                        "updated_at": item.updated_at,
                    }
                )


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
