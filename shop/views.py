import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Product, Order
from cart.models import CartItem
from cart.forms import CheckoutForm


# Create your views here.
def shopHome(request):
    if request.cart:
        print("VIEW HAS CART")
    else:
        print("VIEW NO CART")
    context = {
        'products': Product.objects.all(),
        'form': CheckoutForm()
    }

    return render(request, 'shop/shop.html', context)


def flushCart(request):
    CartItem.objects.filter(cart=request.cart).delete()

    return JsonResponse(data={"status": "ok"}, status=200)


def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            print('valid')
            cart = request.cart
            cart_items = request.cart.items.all()
            new_order = Order.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                shipping_address=form.cleaned_data['shipping_address'],
                phone_number=form.cleaned_data['phone_number']
            )
            cartitems_total = new_order.createOrderItems(cart_items)
            new_order.setSubtotalPrice(cartitems_total)
            new_order.setTotalPrice(cartitems_total)
            new_order.save()
            return redirect('shop:thankYou', new_order.id)
    else:
        return redirect('shop:shopHome')


def thank_you(request, pk):
    return HttpResponse('Thank you page')


