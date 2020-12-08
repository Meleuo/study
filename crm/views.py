from django.shortcuts import render, redirect
from django.views.generic import View
# Create your views here.

from django.contrib import auth
from crm import models
from crm.forms import RegisterForm
from crm import models


class Customer_list(View):

    def get(self, request):
        per_num = 30
        page_num = request.GET.get('page', 1)
        if page_num.isdigit():
            page_num = int(page_num)
        else:
            page_num = 1

        #--> 获取数据的起始和结束值
        start_num = (page_num - 1)*per_num
        stop_num = page_num * per_num

        #--> 获取页数
        all_customer = models.Customer.objects.all()
        all_count, more = divmod(len(all_customer), 30)
        if more:
            all_count = all_count + 1

        return render(request, 'crm/customer_list.html',
                      {'all_customer': all_customer[start_num:stop_num], 'all_count': range(1, all_count + 1), 'page_num': page_num})


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
