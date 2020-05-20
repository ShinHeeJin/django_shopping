from django import forms
from .models import Order
from product.models import Product
from fcuser.models import Fcuser
from django.db import transaction

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
        fcuser = self.request.session.get('user', None) # email

        if quantity and product and fcuser:
            # 트랜젝션 ( 상품 주문 )
            with transaction.atomic():
                prod = Product.objects.get(pk=product)
                order = Order(
                    quantity = quantity,
                    product = Product.objects.get(pk=product),
                    fcuser = Fcuser.objects.get(email=fcuser)
                )
                order.save()

                if prod.stock < quantity or prod.stock == 0:
                    self.product = product
                    self.add_error('quantity','수량을 확인해주세요')
                    return

                prod.stock -= quantity # 재고 계산 ( 재고가 없는 경우 추가 필요 )
                prod.save()
        else:
            self.product = product
            self.add_error('quantity','수량을 입력해 주세요')
            self.add_error('product','수량을 입력해 주세요')            