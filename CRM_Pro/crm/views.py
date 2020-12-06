from django.shortcuts import render, redirect
from django.views.generic import View
# Create your views here.

from django.contrib import auth


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

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
