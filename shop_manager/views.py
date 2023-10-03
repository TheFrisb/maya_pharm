from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from shop.models import Order


# Create your views here.
def redirect_to_dashboard(request):
    return redirect('shop_manager:orderDashboard', "pending")


def dashboard(request):
    context = {
        'orders': Order.objects.filter(status="pending").prefetch_related('items'),
        'template': 'orders'
    }
    return render(request, "shop_manager/base.html", context=context)


def order_dashboard(request, status):
    page_number = request.GET.get("page")
    if status == 'confirmed':
        orders = Order.objects.filter(status="confirmed").prefetch_related('items').order_by('id')
        title = "Потврдани нарачки"
    else:
        orders = Order.objects.filter(status="pending").prefetch_related('items').order_by('-id')
        title = "Непотврдани нарачки"
    paginator = Paginator(orders, 1)
    context = {
        'page_obj': paginator.get_page(page_number),
        'paginator': paginator,
        'title': title,
        'template': 'orders',
    }

    return render(request, "shop_manager/base.html", context=context)
