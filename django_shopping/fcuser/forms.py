from django import forms
from django.contrib.auth.hashers import check_password, make_password
from .models import Fcuser

class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages = {
            'requried' : '이메일을 입력해주세요'
        },
        max_length=64, label="이메일"
    )
    password = forms.CharField(
        error_messages = {
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label="비밀번호"
    )
    re_password = forms.CharField(
        error_messages = {
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label="비밀번호 확인"
    )

    def clean(self):
        cleaned_data = super().clean()  # 값 검증
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        
        if password and re_password:
            # 검증
            if password != re_password:
                self.add_error('password', '비밀번호가 서로 다릅니다.')
                self.add_error('re_password', '비밀번호가 서로 다릅니다.')
            # 회원가입
            else:
                fcuser = Fcuser(
                    email = email,
                    password = make_password(password)
                )
                fcuser.save()

class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages = {
            'requried' : '이메일을 입력해주세요'
        },
        max_length=64, label="이메일"
    )
    password = forms.CharField(
        error_messages = {
            'required' : '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label="비밀번호"
    )
    def clean(self):
        cleaned_data = super().clean()  # 값 검증
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                fcuser = Fcuser.objects.get(email=email)
            except Fcuser.DoesNotExist:
                self.add_error('email', '회원이 존재하지 않습니다.')
                return # 아래를 체크하지 않는다.
                
            # 비밀번호가 틀렸을때
            if not check_password(password, fcuser.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')

            # 비밀번호가 맞았을때(성공)
            else:
                self.email = fcuser.email
