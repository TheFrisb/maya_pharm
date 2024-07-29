import re

from django import forms


class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [("cash", "Плати при достава")]

    first_name = forms.CharField(
        min_length=3,
        max_length=50,
        required=True,
        label="Име",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Вашето Име",
                "class": "checkoutInput",
            }
        ),
    )

    last_name = forms.CharField(
        min_length=3,
        max_length=50,
        required=True,
        label="Презиме",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Вашето Презиме",
                "class": "checkoutInput",
            }
        ),
    )

    shipping_address = forms.CharField(
        min_length=3,
        max_length=50,
        required=True,
        label="Адреса",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Адреса на достава",
                "class": "checkoutInput",
            }
        ),
    )
    city = forms.CharField(
        min_length=2,
        max_length=50,
        required=True,
        label="Град",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Град на достава",
                "class": "checkoutInput",
            }
        ),
    )
    postal_code = forms.CharField(
        min_length=3,
        max_length=10,
        required=True,
        label="Поштенски Код",
        widget=forms.TextInput(
            attrs={
                "class": "checkoutInput",
            }
        ),
    )

    phone_number = forms.CharField(
        min_length=3,
        max_length=15,
        required=True,
        label="Телефонски број",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Вашиот телефонски број",
                "class": "checkoutInput",
            }
        ),
    )

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        required=True,
        label="Payment Method",
        widget=forms.RadioSelect(attrs={"class": "payment_method_radio"}),
        initial="cash",
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        # Check if phone number is valid. You might want to use a more robust
        # regex for real-world usage.
        if not re.match(r"^\+?1?\d{9,15}$", phone_number):
            raise forms.ValidationError("Invalid phone number")

        return phone_number

    def __init__(self, *args, **kwargs):
        """
        Add error class to the input fields if an error is found.
        Used for CSS styling to show states.
        """
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if self.errors.get(name):
                existing_class = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"{existing_class} error".strip()
