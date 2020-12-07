from django.shortcuts import render, redirect
from django.views.generic import View
# Create your views here.

from django.contrib import auth
from crm.forms import RegisterForm
from crm import models


class RegisterView(View):
    def get(self, request):
        form_obj = RegisterForm()
        return render(request, 'register.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = RegisterForm(request.POST)
        if not form_obj.is_valid():
            return render(request, 'register.html', {'form_obj': form_obj})

        '''
        form_obj.cleaned_data.pop('re_password')
        models.UserProfile.objects.create_user(**form_obj.cleaned_data)
        '''
        new_user = form_obj.save()
        new_user.set_password(new_user.password)
        new_user.save()
        return redirect('/login/')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        msg = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = auth.authenticate(request, username=username, password=password)
        if obj:
            return redirect('https://www.baidu.com')
        return render(request, 'login.html', {'msg': '用户名密码错误'})
