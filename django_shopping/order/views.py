from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .forms import RegisterForm
from .models import Order

# Create your views here.
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    # 실패할경우
    def form_invalid(self, form):
        return redirect('/product/' + str(form.product))

    def get_form_kwargs(self, **kwargs):

        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request' : self.request
        })
        return kw

class OrderList(ListView):
    # model = Order # 이렇게 하면 다른사람이 주문한 정보도 볼수 있으므로 queryset을 써야 한다.
    template_name = 'order.html'
    context_object_name = 'order_list'

    # 오버라이딩
    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(fcuser__email = self.request.session.get('user'))
        return queryset