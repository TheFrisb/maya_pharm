import io
import json
from shop.models import Order, OrderItem
import xlsxwriter
from django.http import HttpResponse, JsonResponse
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


def order_export(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
    worksheet = workbook.add_worksheet("Orders")
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'DATA NA PORACKA', bold)
    worksheet.write('B1', 'IME I PREZIME', bold)
    worksheet.write('C1', 'ADRESA', bold)
    worksheet.write('D1', 'GRAD', bold)
    worksheet.write('E1', 'POSTENSKI KOD', bold)
    worksheet.write('F1', 'TELEFON', bold)
    worksheet.write('GA1', 'DOSTAVA', bold)
    worksheet.write('H1', 'VKUPNO', bold)
    header_cols = ['DATA NA PORACKA', 'IME I PREZIME', 'ADRESA', 'GRAD',
                   'POSTENSKI KOD', 'TELEFON', 'DOSTAVA', 'VKUPNO']
    max_col = len(header_cols)
    row = 0
    for col in range(0, max_col):
        worksheet.write(row, col, header_cols[col])
    orders = Order.objects.all()


    workbook.close()
    output.seek(0)
    filename = "django_simple.xlsx"
    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response
