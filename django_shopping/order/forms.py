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
        quantity = cleaned_data.get('quantity',None)
        product = cleaned_data.get('product', None) # id

        if quantity is None:
            # self.add_error('quantity','주문 수량을 입력해주세요')
            return
        
        quantity = int(quantity)

        if quantity < 0:
            self.add_error('quantity','주문 수량을 확인해주세요')
            return 

        if quantity == 0:
            self.add_error('quantity','하나 이상 주문해주세요')
            return

        stock = Product.objects.get(pk=product).stock

        if stock == 0:
            self.add_error('quantity','재고가 없습니다.')
            return

        if quantity > stock:
            self.add_error('quantity','재고보다 많은 수량을 주문하셨습니다.')
            return 

          