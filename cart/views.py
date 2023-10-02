import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import CartItemForm, UpdateCartItemForm


# Create your views here.
@require_http_methods(['POST'])
def addToCart(request):
    try:
        form = CartItemForm(json.loads(request.body))
    except json.JSONDecodeError:
        return JsonResponse(data={
            'success': 'error',
            'message': 'Expected contentType: "application/json"'
        }, status=400)
    if form.is_valid():
        cart = request.cart
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']
        if not quantity:
            cart_item = cart.add_product(product)
        else:
            cart_item = cart.add_product(product, quantity)

        return JsonResponse(data={
            'success': 'success',
            'message': "Product added to cart",
            'cart': cart.as_dict(),
            'cartItem': cart_item.as_dict()
        }, status=200)

    else:
        return JsonResponse({
            'success': 'error',
            'errors': form.errors
        }, status=400)


@require_http_methods(['POST'])
def removeFromCart(request):
    form = CartItemForm(request.body)

    if form.is_valid():
        cart = request.cart
        cart.remove_product(form.cleaned_data['product'])
        return JsonResponse(data={
            'success': 'success',
            'message': "Product removed from cart",
            'cart': cart.as_dict(),
        }, status=200)

    else:
        return JsonResponse({
            'success': 'error',
            'errors': form.errors
        }, status=400)


@require_http_methods(['POST'])
def updateCartItem(request):
    form = UpdateCartItemForm(request.body)

    if form.is_valid():
        cart = request.cart
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']

        cart.update_product(product, quantity)

        return JsonResponse(data={
            'success': 'success',
            'message': "Product updated in cart",
            'cart': cart.as_dict(),
        }, status=200)


    else:
        return JsonResponse({
            'success': 'error',
            'errors': form.errors
        }, status=400)
