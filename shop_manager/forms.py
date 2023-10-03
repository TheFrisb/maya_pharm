from django import forms
from shop.models import Order


class OrderForm(forms.Form):
    order = forms.ModelChoiceField(queryset=Order.objects.all())
