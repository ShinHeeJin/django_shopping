from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView  
from .models import Product
from .forms import RegisterForm
from fcuser.decorator import admin_required
from order.forms import RegisterForm as OrderForm
# Create your views here.
class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = "product_list"

@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name = form.data.get('name'),
            price = form.data.get('price'),
            description = form.data.get('description'),
            stock = form.data.get('stock')
        )
        product.save()
        # 오버라이딩을 했기때문에 부모생성자 필요
        return super().form_valid(form)

class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all() # 필터링 추가 가능
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request)
        return context

