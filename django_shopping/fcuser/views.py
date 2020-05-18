from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import LoginForm, RegisterForm

# Create your views here.

def index(request):
    return render(request, 'index.html', {'email':request.session.get('user')})

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/' # 성공했을때 구현

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/' # 성공했을때 구현

    def form_valid(self, form): # 유효성 검사가 끝났을때 들어오는 함수(세션저장)
        self.request.session['user'] = form.email
        return super().form_valid(form)
