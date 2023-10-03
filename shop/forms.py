from django import forms
import re


class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = (
        ('card', 'Credit card'),
        ('cash', 'Cash on delivery')
    )

    first_name = forms.CharField(
        min_length=3,
        max_length=50,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'checkoutInput',
        })
    )

    last_name = forms.CharField(
        min_length=3,
        max_length=50,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'checkoutInput',
        })
    )

    shipping_address = forms.CharField(
        min_length=3,
        max_length=50,
        required=True,
        label='Address',
        widget=forms.TextInput(attrs={
            'placeholder': 'Address',
            'class': 'checkoutInput',
        })
    )
    city = forms.CharField(
        min_length=2,
        max_length=50,
        required=True,
        label='City',
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
            'class': 'checkoutInput',
        })
    )
    postal_code = forms.CharField(
        min_length=3,
        max_length=10,
        required=True,
        label='Postal Code',
        widget=forms.TextInput(attrs={
            'placeholder': 'Postal Code',
            'class': 'checkoutInput',
        })
    )

    phone_number = forms.CharField(
        min_length=3,
        max_length=15,
        required=True,
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number',
            'class': 'checkoutInput',
        })
    )

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        required=True,
        label='Payment Method',
        widget=forms.RadioSelect(attrs={'class': 'payment_method_radio'}),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Check if phone number is valid. You might want to use a more robust
        # regex for real-world usage.
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise forms.ValidationError('Invalid phone number')

        return phone_number

    def __init__(self, *args, **kwargs):
        """
        Add error class to the input fields if an error is found.
        Used for CSS styling to show states.
        """
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if self.errors.get(name):
                existing_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_class} error".strip()
