from django.shortcuts import render, redirect
from shop.models import Order

# Create your views here.
def redirect_to_dashboard(request):
    return redirect('shop_manager:dashboard')


def dashboard(request):
    context = {
        'orders': Order.objects.filter(status="Pending").prefetch_related('items'),
        'template': 'orders'
    }
    return render(request, "shop_manager/base.html", context=context)
