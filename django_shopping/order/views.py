from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import FormView
from fcuser.decorator import login_required
from .forms import RegisterForm
from .models import Order


@method_decorator(login_required, name='dispatch')
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