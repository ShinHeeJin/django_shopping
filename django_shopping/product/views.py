from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView  

from .serializer import ProductSerializer
from rest_framework import generics
from rest_framework import mixins
from .models import Product
from .forms import RegisterForm
from fcuser.decorator import admin_required
from order.forms import RegisterForm as OrderForm

class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):

    serializer_class = ProductSerializer # 데이터 검증을 위해서

    def get_queryset(self): # 어떤 데이터를 활용할 것인지에대한
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs) # ListModelMixin에 있는 함수

class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin): # 상세보기를 위한 mixin

    serializer_class = ProductSerializer # 데이터 검증을 위해서

    def get_queryset(self): # 어떤 데이터를 활용할 것인지에대한
        return Product.objects.all().order_by('id') # pk를 통해 하나만 제공하기 때문에 all query set을 가져온다

    def get(self, request, *args, **kwargs): # get 요청이 왔을때 상세정보를 요청하고 싶다.
        return self.retrieve(request, *args, **kwargs) # ListModelMixin에 있는 함수

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

