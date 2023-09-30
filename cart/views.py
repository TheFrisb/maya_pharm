from rest_framework import views
from .serializers import CartItemSerializer, CartSerializer, ProductSerializer
from .utils import create_error_response, create_success_response


class CartView(views.APIView):

    def post(self, request, *args, **kwargs):
        # Add to cart
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            cart = request.cart

            cart.add_product(product, quantity)
            return create_success_response(CartSerializer(cart).data, "Product added to cart")
        return create_error_response(serializer.errors)

    def put(self, request, *args, **kwargs):
        # Update cart item
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            cart = request.cart

            cart.update_product(product, quantity)
            return create_success_response(CartSerializer(cart).data, "Product updated in cart")
        return create_error_response(serializer.errors)

    def delete(self, request, *args, **kwargs):
        # Remove from cart
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data.get('product')
            if not product:
                return create_error_response({'success': 'error', 'errors': 'No such product exists'})
            cart = request.cart

            cart.remove_product(product)
            return create_success_response(CartSerializer(cart).data, "Product removed from cart")
        return create_error_response(serializer.errors)
