import json

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import CartItemForm, UpdateCartItemForm


def parse_json_request(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, json_error('Expected contentType: "application/json"', status=400)


@require_http_methods(["POST"])
def addToCart(request):
    request_data, error = parse_json_request(request)
    if error:
        return error

    form = CartItemForm(request_data)
    if not form.is_valid():
        return json_error("Invalid data", {"errors": form.errors})

    cart = request.cart
    product = form.cleaned_data["product"]
    quantity = form.cleaned_data.get("quantity", 1)  # Default to 1 if not specified

    cart_item = cart.add_product(product, quantity)
    data = {"cart": cart.refresh_and_get_details(), "cartItem": cart_item.as_dict()}
    return json_success("Product added to cart", data)


@require_http_methods(["POST"])
def removeFromCart(request):
    request_data, error = parse_json_request(request)
    if error:
        return error

    form = CartItemForm(request_data)
    if form.is_valid():
        cart = request.cart
        cart.remove_product(form.cleaned_data["product"])
        cart.refresh_from_db()  # Make sure to refresh cart after modification
        return json_success("CartItem removed from cart", {"cart": cart.as_dict()})
    else:
        return json_error("Invalid data", {"errors": form.errors})


@require_http_methods(["POST"])
def updateCartItem(request):
    request_data, error = parse_json_request(request)
    if error:
        return error

    form = UpdateCartItemForm(request_data)
    if form.is_valid():
        cart = request.cart
        product = form.cleaned_data["product"]
        quantity = form.cleaned_data["quantity"]

        with transaction.atomic():
            if cart.update_product(product, quantity):
                cart.refresh_from_db()  # Refresh the cart after updates
                return json_success("Product updated in cart", {"cart": cart.as_dict()})
            else:
                return json_error("Product not found in cart", status=404)
    else:
        return json_error("Invalid data", {"errors": form.errors})


def json_error(message, data=None, status=400):
    response = {"success": "error", "message": message}
    if data:
        response.update(data)
    return JsonResponse(response, status=status)


def json_success(message, data=None, status=200):
    response = {"success": "success", "message": message}
    if data:
        response.update(data)
    return JsonResponse(response, status=status)
