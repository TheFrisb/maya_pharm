from django import forms
from shop.models import Product
import re


class CartItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(min_value=1, required=False)


class UpdateCartItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField()


class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )

    last_name = forms.CharField(
        max_length=50,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    shipping_address = forms.CharField(
        max_length=255,
        required=True,
        label='Address',
        widget=forms.Textarea(attrs={'placeholder': 'Address'})
    )

    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label='Phone Number',
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Check if phone number is valid. You might want to use a more robust
        # regex for real-world usage.
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise forms.ValidationError('Invalid phone number format. Use format: +999999999. Up to 15 digits allowed.')

        return phone_number
