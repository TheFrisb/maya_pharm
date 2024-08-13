from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from shop.models import Order


# Create your views here.
@staff_member_required
def redirect_to_dashboard(request):
    return redirect("shop_manager:orderDashboard", "pending")


@staff_member_required
def dashboard(request):
    context = {
        "orders": Order.objects.filter(status="pending").prefetch_related("items"),
        "template": "orders",
    }
    return render(request, "shop_manager/base.html", context=context)


@staff_member_required
def order_dashboard(request, status):
    page_number = request.GET.get("page")
    if status == "confirmed":
        orders = (
            Order.objects.filter(status="confirmed")
            .prefetch_related("items")
            .order_by("id")
        )
        title = "Потврдани нарачки"
    elif status == "deleted":
        orders = (
            Order.objects.filter(status="deleted")
            .prefetch_related("items")
            .order_by("id")
        )
        title = "Избришени нарачки"
    else:
        orders = (
            Order.objects.filter(status="pending")
            .prefetch_related("items")
            .order_by("-id")
        )
        title = "Непотврдани нарачки"
    paginator = Paginator(orders, 8)
    context = {
        "page_obj": paginator.get_page(page_number),
        "paginator": paginator,
        "title": title,
        "template": "orders",
    }

    return render(request, "shop_manager/base.html", context=context)
