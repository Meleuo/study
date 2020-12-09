import copy
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import View
from django.utils.safestring import mark_safe
from django.contrib import auth
from django.db.models import Q
from django.http import QueryDict

from crm import models
from crm.forms import RegisterForm
from crm.forms import CustomerForm
from crm.forms import ConsultRecordForm
from utils.pagination import Pagination


class ConsultRecord(View):
    def get(self, request, id=None):
        obj = models.ConsultRecord.objects.filter(id=id).first() or models.ConsultRecord(consultant=request.user)
        form_obj = ConsultRecordForm(instance=obj)
        return render(request, 'crm/consult_record_add.html', {'form_obj': form_obj})

    def post(self, request, id=None):
        form_obj = ConsultRecordForm(request.POST, instance=models.ConsultRecord(consultant=request.user))
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_record_list'))
        return render(request, 'crm/consult_record_add.html', {'form_obj': form_obj})

# --> 编辑跟进记录
class ConsultRecord_edit(View):
    def get(self, request, id=None):
        obj = models.ConsultRecord.objects.filter(id=id).first()
        form_obj = ConsultRecordForm(instance=obj)
        return render(request, 'crm/consult_record_add.html', {'form_obj': form_obj})

    def post(self, request, id=None):
        obj = models.ConsultRecord.objects.filter(id=id).first()
        form_obj = ConsultRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_record_list'))
        return render(request, 'crm/consult_record_add.html', {'form_obj': form_obj})


# --> 添加跟进记录
class ConsultRecord_add(View):
    def get(self, request):
        form_obj = ConsultRecordForm(instance=models.ConsultRecord(consultant=request.user))
        return render(request, 'crm/consult_record_add.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = ConsultRecordForm(request.POST, instance=models.ConsultRecord(consultant=request.user))
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_record_list'))
        return render(request, 'crm/consult_record_add.html', {'form_obj': form_obj})


# --> 跟进记录列表
class ConsultRecord_list(View):
    def get(self, request, id=None):
        all_consult_record = models.ConsultRecord.objects.filter(delete_status=False)
        return render(request, 'crm/consult_record_list.html', {
            'all_consult_record': all_consult_record,
        })


# --> 客户编辑视图
class Customer(View):
    def get(self, request, id=None):
        edit_obj = models.Customer.objects.filter(id=id).first()
        form_obj = CustomerForm(instance=edit_obj)
        return render(request, 'crm/customer.html', {'form_obj': form_obj, 'id': id})

    def post(self, request, id=None):
        next_url = request.GET.get('next', None)
        edit_obj = models.Customer.objects.filter(id=id).first()
        form_obj = CustomerForm(request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            if next_url:
                return redirect(next_url)
            return redirect(reverse('customer_list'))

        return render(request, 'crm/customer.html', {'form_obj': form_obj}, )


# class Customer_edit(View):
#     def get(self, request, id):
#         edit_obj = models.Customer.objects.filter(id=id).first()
#         if edit_obj:
#             form_obj = CustomerForm(instance=edit_obj)
#             return render(request, 'crm/customer_edit.html', {'form_obj': form_obj})
#
#     def post(self, request, id):
#         edit_obj = models.Customer.objects.filter(id=id).first()
#         form_obj = CustomerForm(request.POST, instance=edit_obj)
#         if form_obj.is_valid():
#             form_obj.save()
#             return redirect(reverse('customer_list'))
#         return render(request, 'crm/customer_edit.html', {'form_obj': form_obj})
#
#
# class Customer_add(View):
#     def get(self, request):
#         form_obj = CustomerForm()
#         return render(request, 'crm/customer_add.html', {'form_obj': form_obj})
#
#     def post(self, request):
#         form_obj = CustomerForm(request.POST)
#         if form_obj.is_valid():
#             print('校验成功')
#             form_obj.save()
#             return redirect(reverse('customer_list'))
#         return render(request, 'crm/customer_add.html', {'form_obj': form_obj})

# --> 客户展示视图
class Customer_list(View):
    def get(self, request, option_ret=False):

        q = self.get_search_contion(['qq', 'qq_name'])
        print(' -' * 10)
        print(q)
        if request.path_info == reverse('customer_list'):
            # --> 公户
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True).order_by('-date')
            url = reverse('customer_list')
            title = '公户列表'

        else:
            # --> 私户my_customer
            all_customer = models.Customer.objects.filter(q, consultant=request.user).order_by('-date')
            url = reverse('my_customer_list')
            title = '私户列表'

        page_num = request.GET.get('page', 1)
        search_params = copy.deepcopy(request.GET)
        search_params._mutable = True  # --> 允许request.GET 可有修改, 在QueryDict源代码中可有找到相关的对应内容
        # from  django.http import QueryDict

        pagination_obj = Pagination(search_params, page_num=page_num, len_customer=len(all_customer), url=url)

        # --> 生成一个QueryDict对象
        nextqd = QueryDict()
        nextqd._mutable = True  # --> QueryDict对象 可写
        nextqd['next'] = request.get_full_path()  # --> 获取当前页面的完整URl 放到nextqd中

        return render(request, 'crm/customer_list.html', {
            'all_customer': all_customer[pagination_obj.start:pagination_obj.end],
            'html_page': mark_safe(pagination_obj.show_html),
            'title': title,
            'option_ret': option_ret if option_ret else False,
            'next': nextqd.urlencode()  # --> 借助QueryDict的urlencode方法自动转义url中的特殊符号传递给模板
        })

    def post(self, request):
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        option_ret = getattr(self, action)()
        return self.get(request, option_ret=option_ret)

    def option_put_private(self):
        # --> 公户变私户
        request = self.request
        ids = request.POST.getlist('id')

        # --> 一对多正向操作
        # models.Customer.objects.filter(id__in=ids).update(consultant=request.user)

        # --> 一对多反向操作
        request.user.customers.add(*models.Customer.objects.filter(id__in=ids))

        return True

    def option_put_public(self):
        # --> 公户变私户
        request = self.request
        ids = request.POST.getlist('id')

        # --> 一对多正向操作
        # models.Customer.objects.filter(id__in=ids).update(consultant=None)

        # --> 一对多反向操作
        request.user.customers.remove(*models.Customer.objects.filter(id__in=ids))

        return True

    # def option_put_private(self):

    def get_search_contion(self, search_list):
        search_content = self.request.GET.get('search', '')
        q = Q()
        q.connector = 'OR'
        for i in search_list:
            q.children.append(Q((
                '%s__contains' % i, search_content
            )))
        return q


# --> 系统注册
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
        new_user.is_superuser = True
        new_user.is_staff = True
        new_user.save()
        return redirect('/login/')


# --> 系统登陆
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        msg = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = auth.authenticate(request, username=username, password=password)
        if obj:
            auth.login(request, obj)
            return redirect(reverse('my_customer_list'))
        return render(request, 'login.html', {'msg': '用户名密码错误'})
