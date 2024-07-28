from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from cart.middleware import CartMiddleware
from .forms import CheckoutForm
from .models import Product, Order, Category, Brand


def shop_home(request):
    context = {
        "products": Product.objects.all()[0:24],
        "title": "Почетна",
        "brands": Brand.objects.annotate(product_count=Count("products")).filter(
            product_count__gt=0
        ),
        "pain_category": Category.objects.filter(slug="protiv-bolka").first(),
        "vitamin_category": Category.objects.filter(
            slug="vitamini-i-suplementi"
        ).first(),
    }
    return render(request, "shop/shop.html", context)


def product_page(request, name):
    product = get_object_or_404(Product.objects.select_related(), slug=name)
    related_products = Product.objects.filter(
        categories__in=product.categories.all()
    ).exclude(id=product.id)

    # Check if there are less than 8 related products
    if related_products.count() < 8:
        more_products = Product.objects.all().exclude(id=product.id)[:8]
        related_products = (
            list(related_products) + list(more_products)[: 8 - related_products.count()]
        )

    context = {
        "product": product,
        "related_products": related_products,
        "title": product.title,
    }
    return render(request, "shop/product_page.html", context)


def category_page(request, slug):
    category = get_object_or_404(
        Category.objects.prefetch_related("products"), slug=slug
    )
    context = {
        "category": category,
        "products": category.products.all(),
        "title": category.name,
    }
    return render(request, "shop/category_page.html", context)


def brand_view(request, slug):
    brand = get_object_or_404(Brand.objects.prefetch_related("products"), slug=slug)
    context = {
        "category": brand,
        "products": brand.products.all(),
        "title": brand.name,
    }
    return render(request, "shop/category_page.html", context)


def checkout(request):
    if request.method == "POST":
        middleware = CartMiddleware(get_response=None)
        post_form = CheckoutForm(request.POST)
        if not post_form.is_valid():
            context = {"form": post_form, "title": "Кон нарачка"}
            return render(request, "shop/checkout.html", context)

        cart = request.cart
        cart_items = request.cart.items.all()
        new_order = Order.objects.create(
            first_name=post_form.cleaned_data["first_name"],
            last_name=post_form.cleaned_data["last_name"],
            shipping_address=post_form.cleaned_data["shipping_address"],
            phone_number=post_form.cleaned_data["phone_number"],
        )
        cartitems_total = new_order.createOrderItems(cart_items)
        cart.delete()
        middleware.get_cart(request)
        new_order.setSubtotalPrice(cartitems_total)
        new_order.setTotalPrice(cartitems_total)
        new_order.save()
        return redirect("shop:thank_you_page")

    else:
        if request.cart.items_count == 0:
            return redirect("shop:shop_home")
        form = CheckoutForm()
        context = {"form": form, "title": "Кон нарачка"}
        return render(request, "shop/checkout.html", context)


def thank_you_page(request):
    context = {"title": "Ви благодариме за вашата нарачка!"}
    return render(request, "shop/thank_you_page.html", context)


def product_titles(request):
    query = request.GET.get("q", "")  # Get the query parameter from the URL
    products = Product.objects.filter(title__icontains=query)[:3]
    products_data = [
        {"title": product.title, "url": product.get_absolute_url()}
        for product in products
    ]
    return JsonResponse({"products": products_data})
