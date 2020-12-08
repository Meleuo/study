from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import View
from django.utils.safestring import mark_safe
from django.contrib import auth

from crm import models
from crm.forms import RegisterForm
from crm.forms import CustomerForm
from utils.pagination import Pagination


class Customer(View):
    def get(self, request, id=None):
        edit_obj = models.Customer.objects.filter(id=id).first()
        # if edit_obj:
        form_obj = CustomerForm(instance=edit_obj)
        return render(request, 'crm/customer.html', {'form_obj': form_obj, 'id': id})

    def post(self, request, id=None):
        edit_obj = models.Customer.objects.filter(id=id).first()
        form_obj = CustomerForm(request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
        return render(request, 'crm/customer.html', {'form_obj': form_obj}, )


class Customer_edit(View):
    def get(self, request, id):
        edit_obj = models.Customer.objects.filter(id=id).first()
        if edit_obj:
            form_obj = CustomerForm(instance=edit_obj)
            return render(request, 'crm/customer_edit.html', {'form_obj': form_obj})

    def post(self, request, id):
        edit_obj = models.Customer.objects.filter(id=id).first()
        form_obj = CustomerForm(request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
        return render(request, 'crm/customer_edit.html', {'form_obj': form_obj})


class Customer_add(View):
    def get(self, request):
        form_obj = CustomerForm()
        return render(request, 'crm/customer_add.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = CustomerForm(request.POST)
        if form_obj.is_valid():
            print('校验成功')
            form_obj.save()
            return redirect(reverse('customer_list'))
        return render(request, 'crm/customer_add.html', {'form_obj': form_obj})


class Customer_list(View):
    def get(self, request):
        all_customer = models.Customer.objects.all().order_by('-date')
        page_num = request.GET.get('page', 1)

        pagination_obj = Pagination(page_num=page_num, len_customer=len(all_customer), url=reverse('customer_list'))

        return render(request, 'crm/customer_list.html', {
            'all_customer': all_customer[pagination_obj.start:pagination_obj.end],
            'html_page': mark_safe(pagination_obj.show_html)
        })


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
