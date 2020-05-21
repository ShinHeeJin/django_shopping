from django import forms
from .models import Order
from product.models import Product
from fcuser.models import Fcuser


class RegisterForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required':'수량을 입력해주세요.'
        },
        label='수량'
    )

    product = forms.IntegerField(
        error_messages={
            'required':'상품을 입력해주세요'
        }, label='상품', widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product') # id

        if not (quantity and product):
            self.add_error('quantity','수량을 입력해 주세요')
            self.add_error('product','수량을 입력해 주세요')            