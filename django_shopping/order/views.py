from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.db import transaction
from fcuser.decorator import login_required
from .forms import RegisterForm
from .models import Order
from product.models import Product
from fcuser.models import Fcuser

@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        # 트랜젝션 ( 상품 주문 )
        with transaction.atomic():
            prod = Product.objects.get(pk=form.data.get('product'))
            quantity = int(form.data.get('quantity'))
            email = self.request.session.get('user')
            fcuser = Fcuser.objects.get(email=email)

            # 주문생성
            order = Order(
                quantity = quantity,
                fcuser = fcuser,
                product = prod
            )
            order.save() # 저장
            prod.stock -= quantity # 재고 계산 ( 재고가 없는 경우 추가 필요 )
            prod.save()

        return super().form_valid(form)

    # 실패할경우
    def form_invalid(self, form):
        product = form.data.get('product')
        res_data = {
            'form':form,
            'product':Product.objects.get(pk=product)
        }
        return render(self.request, f'product_detail.html', res_data)

    def get_form_kwargs(self, **kwargs):

        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request' : self.request
        })
        return kw
        
@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    # model = Order # 이렇게 하면 다른사람이 주문한 정보도 볼수 있으므로 queryset을 써야 한다.
    template_name = 'order.html'
    context_object_name = 'order_list'

    # 오버라이딩
    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(fcuser__email = self.request.session.get('user'))
        return queryset

    # def dispatch(request, *args, **kwargs)