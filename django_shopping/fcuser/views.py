from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .models import Fcuser
from .forms import LoginForm, RegisterForm

# Create your views here.

def index(request):
    return render(request, 'index.html', {'email':request.session.get('user')})

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/' # 성공했을때 구현

    def form_valid(self, form): # 유효성 검사가 끝났을때 호출되는 함수
        fcuser = Fcuser(
            email = form.data.get('email'),
            password = make_password(form.data.get('password')),
            lavel='user'
        )
        fcuser.save()
        return super().form_valid(form)
        


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/' # 성공했을때 구현

    def form_valid(self, form): # 유효성 검사가 끝났을때 들어오는 함수(세션저장)
        self.request.session['user'] = form.data.get('email') # 이메일 저장
        return super().form_valid(form)
        # form_valid는 django.http.HttpResponse를 반환한다.
        # 유효한 폼데이터가 POST 요청되었을 때 form_valid 메소드가 호출된다. form_valid는 단순히 success_url로의 연결을 수행한다.

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/')