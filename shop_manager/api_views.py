import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import OrderForm


# Create your views here.
@require_http_methods(['POST'])
def confirmOrder(request):
    try:
        form = OrderForm(json.loads(request.body))
    except json.JSONDecodeError:
        return JsonResponse(data={
            'success': 'error',
            'message': 'Expected contentType: "application/json"'
        }, status=400)
    if form.is_valid():
        order = form.cleaned_data.get('order')
        order.set_to_confirm()

        return JsonResponse(data={
            'success': 'success',
            'message': "Order updated",
        }, status=200)

    else:
        return JsonResponse({
            'success': 'error',
            'errors': form.errors
        }, status=400)


@require_http_methods(['POST'])
def deleteOrder(request):
    try:
        form = OrderForm(json.loads(request.body))
    except json.JSONDecodeError:
        return JsonResponse(data={
            'success': 'error',
            'message': 'Expected contentType: "application/json"'
        }, status=400)
    if form.is_valid():
        order = form.cleaned_data.get('order')
        order.set_to_deleted()

        return JsonResponse(data={
            'success': 'success',
            'message': "Order updated",
        }, status=200)

    else:
        return JsonResponse({
            'success': 'error',
            'errors': form.errors
        }, status=400)


@require_http_methods(['POST'])
def restoreOrder(request):
    try:
        form = OrderForm(json.loads(request.body))
    except json.JSONDecodeError:
        return JsonResponse(data={
            'success': 'error',
            'message': 'Expected contentType: "application/json"'
        }, status=400)
    if form.is_valid():
        order = form.cleaned_data.get('order')
        order.set_to_pending()

        return JsonResponse(data={
            'success': 'success',
            'message': "Order updated",
        }, status=200)

    else:
        return JsonResponse({
            'success': 'error',
            'errors': form.errors
        }, status=400)
