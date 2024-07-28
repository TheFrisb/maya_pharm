from django.db.models import Prefetch

from .models import Cart, CartItem


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.cart = self.get_cart(request)
        response = self.get_response(request)
        return response

    def get_cart(self, request):
        cart_id = request.session.get("cart_id")
        if cart_id:
            # Prefetch items and their associated products
            items_prefetch = Prefetch(
                "items", queryset=CartItem.objects.select_related("product")
            )
            cart = (
                Cart.objects.prefetch_related(items_prefetch).filter(id=cart_id).first()
            )
            if cart:
                return cart

        # Create a new cart if not found
        return self.create_new_cart(request)

    def create_new_cart(self, request):
        cart = Cart.objects.create()
        request.session["cart_id"] = cart.id
        return cart
