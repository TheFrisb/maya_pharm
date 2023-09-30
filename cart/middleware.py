from .models import Cart

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
            if cart:
                request.cart = cart
            else:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
                request.cart = cart
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
            request.cart = cart

        response = self.get_response(request)
        return response
