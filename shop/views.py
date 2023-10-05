from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order
from .forms import CheckoutForm


# Create your views here.
def shop_home(request):
    if request.cart:
        print("VIEW HAS CART")
    else:
        print("VIEW NO CART")
    context = {
        'products': Product.objects.all(),
        'form': CheckoutForm()
    }

    return render(request, 'shop/shop.html', context)


def product_page(request):
    context = {}
    return render(request, 'shop/product_page.html', context)


def checkout(request):
    if request.method == 'POST':
        post_form = CheckoutForm(request.POST)
        if not post_form.is_valid():
            context = {
                'form': post_form
            }
            return render(request, 'shop/checkout.html', context)

        cart = request.cart
        cart_items = request.cart.items.all()
        new_order = Order.objects.create(
            first_name=post_form.cleaned_data['first_name'],
            last_name=post_form.cleaned_data['last_name'],
            shipping_address=post_form.cleaned_data['shipping_address'],
            phone_number=post_form.cleaned_data['phone_number']
        )
        cartitems_total = new_order.createOrderItems(cart_items)
        new_order.setSubtotalPrice(cartitems_total)
        new_order.setTotalPrice(cartitems_total)
        new_order.save()
        return redirect('shop:thank_you', new_order.id)

    else:
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(request, 'shop/checkout.html', context)


def thank_you(request, pk):
    return HttpResponse('Thank you page')
