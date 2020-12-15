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
from crm.forms import EnrollmentForm
from utils.pagination import Pagination
from django.db import transaction


class Enrollment(View):
    def get(self, request):
        customer_id = request.GET.get('customer_id', '0')

        enrollment_id = request.GET.get('enrollment_id', '0')

        if customer_id != '0':
            customer = models.Customer.objects.filter(id=customer_id).first()
            obj = models.Enrollment(
                customer_id=customer_id, enrolment_class=customer.class_list.all().first())

            # --> 模板的Title
            title = '添加 %s的报名记录' % customer

        # --> 如果consultrecord_id能查到实际的数据, 那么则意味着这次的操作上一次修改 跟进记录 的操作
        elif models.Enrollment.objects.filter(id=int(enrollment_id)):
            obj = models.Enrollment.objects.filter(
                id=int(enrollment_id)).first()
            title = '修改 %s报名记录' % obj.customer

        else:  # --> 剩下的最后一个情况就是添加跟进记录
            title = '添加报名记录'
            obj = models.Enrollment(customer=request.user.customers.first())
            print(obj)

        # --> 将obj传递给Form, 生成表单
        form_obj = EnrollmentForm(instance=obj)
        return render(request, 'crm/customer/enrollment.html', {'form_obj': form_obj, 'title': title})

    def post(self, request):
        # --> 保存操作就只区分 修改保存, 和新建保存了
        enrollment_id = request.GET.get('enrollment_id', '0')
        # customer_id = request.GET.get('customer_id', '0')

        next_url = request.GET.get('next', None)  # --> 获取操作完成后的跳转页面
        obj = models.Enrollment.objects.filter(id=int(enrollment_id)).first() or models.Enrollment(
            customer=request.user.customers.first())

        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            if next_url:
                return redirect(next_url)
            # --> 不存在的情况下就跳转到consult_record_list
            return redirect(reverse('consult_record_list'))
        return render(request, 'crm/customer/enrollment.html', {'form_obj': form_obj})


# --> 报名列表
class Enrollment_list(View):
    def get(self, request):
        customer_id = request.GET.get('customer_id', 0)
        if customer_id != 0:
            all_enrollment = models.Enrollment.objects.filter(
                customer_id=customer_id)
            title = '%s报名记录' % models.Customer.objects.filter(
                id=customer_id).first()

        else:
            all_enrollment = models.Enrollment.objects.all()
            title = '全部报名记录'

        # --> 生成一个QueryDict对象
        nextqd = QueryDict()
        nextqd._mutable = True  # --> QueryDict对象 可写
        nextqd['next'] = request.get_full_path()  # --> 获取当前页面的完整URl 放到nextqd中
        return render(request, 'crm/customer/enrollment_list.html',
                      {'all_enrollment': all_enrollment,
                       'customer_id': customer_id,
                       'next': nextqd.urlencode(),
                       'title': title
                       })


# --> 跟进记录添加 + 编辑表
class ConsultRecord(View):
    def get(self, request):
        '''
           customer_id 会在私户列表中的 跟进记录 a标签中附带, customer_id对应的上一个客户ID, 通过传递客户ID确认这个请求上一个只显示
       指定用户的跟进记录列表
        '''
        customer_id = request.GET.get('customer_id', '0')

        '''
        consultrecord_id 是编辑 跟进记录时传递过来的 跟进记录ID
        '''
        consultrecord_id = request.GET.get('consultrecord_id', '0')

        # --> 判断customer_id是否为0(默认为0), 不为0则这次请求是一个添加指定客户 跟进记录的操作
        if customer_id != '0':
            # -->实例化一个ConsultRecord(跟进记录)的对象, 将当前用户和, 需要修改的客户ID传递给对象, customer_id在跟进记录的表中就是对应着客户
            obj = models.ConsultRecord(
                customer_id=customer_id, consultant=request.user)

            # --> 模板的Title
            customer = models.Customer.objects.filter(id=customer_id).first()
            title = '添加 %s的跟进记录' % customer

        # --> 如果consultrecord_id能查到实际的数据, 那么则意味着这次的操作上一次修改 跟进记录 的操作
        elif models.ConsultRecord.objects.filter(id=int(consultrecord_id)):
            obj = models.ConsultRecord.objects.filter(
                id=int(consultrecord_id)).first()
            title = '修改 %s跟进记录' % obj.customer

        else:  # --> 剩下的最后一个情况就是添加跟进记录
            title = '添加跟进记录'
            obj = models.ConsultRecord(consultant=request.user)

        # --> 将obj传递给Form, 生成表单
        form_obj = ConsultRecordForm(instance=obj)
        return render(request, 'crm/customer/consult_record.html', {'form_obj': form_obj, 'title': title})

    def post(self, request):
        # --> 保存操作就只区分 修改保存, 和新建保存了
        consultrecord_id = request.GET.get('consultrecord_id', '0')
        next_url = request.GET.get('next', None)  # --> 获取操作完成后的跳转页面
        obj = models.ConsultRecord.objects.filter(id=int(consultrecord_id)).first() or models.ConsultRecord(
            consultant=request.user)

        form_obj = ConsultRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            if next_url:
                return redirect(next_url)
            # --> 不存在的情况下就跳转到consult_record_list
            return redirect(reverse('consult_record_list'))
        return render(request, 'crm/customer/consult_record.html', {'form_obj': form_obj})


'''编辑跟进记录&添加跟进记录
# --> 编辑跟进记录
class ConsultRecord_edit(View):
    def get(self, request, id=None):
        obj = models.ConsultRecord.objects.filter(id=id).first()
        form_obj = ConsultRecordForm(instance=obj)
        return render(request, 'customer/consult_record_add.html', {'form_obj': form_obj})

    def post(self, request, id=None):
        obj = models.ConsultRecord.objects.filter(id=id).first()
        form_obj = ConsultRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_record_list'))
        return render(request, 'customer/consult_record_add.html', {'form_obj': form_obj})


# --> 添加跟进记录
class ConsultRecord_add(View):
    def get(self, request):
        form_obj = ConsultRecordForm(instance=models.ConsultRecord(consultant=request.user))
        return render(request, 'customer/consult_record_add.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = ConsultRecordForm(request.POST, instance=models.ConsultRecord(consultant=request.user))
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('consult_record_list'))
        return render(request, 'customer/consult_record_add.html', {'form_obj': form_obj})
'''


# --> 跟进记录显示列表
class ConsultRecord_list(View):
    def get(self, request):
        customer_id = request.GET.get('customer_id', '0')
        if customer_id == '0':
            all_consult_record = models.ConsultRecord.objects.filter(
                delete_status=False, consultant=request.user)
            title = '全部客户跟进记录'
        else:
            all_consult_record = models.ConsultRecord.objects.filter(delete_status=False, customer_id=customer_id,
                                                                     consultant=request.user)
            customer = models.Customer.objects.filter(id=customer_id).first()
            title = '%s 跟进记录' % (customer)

        # --> 生成一个QueryDict对象
        nextqd = QueryDict()
        nextqd._mutable = True  # --> QueryDict对象 可写
        nextqd['next'] = request.get_full_path()  # --> 获取当前页面的完整URl 放到nextqd中

        return render(request, 'crm/customer/consult_record_list.html', {
            'all_consult_record': all_consult_record,
            'title': title,
            'customer_id': customer_id,
            'next': nextqd.urlencode()
        })


# --> 客户编辑视图
class Customer(View):
    def get(self, request, id=None):
        edit_obj = models.Customer.objects.filter(id=id).first()
        form_obj = CustomerForm(instance=edit_obj)
        return render(request, 'crm/customer/customer.html', {'form_obj': form_obj, 'id': id})

    def post(self, request, id=None):
        next_url = request.GET.get('next', None)
        edit_obj = models.Customer.objects.filter(id=id).first()
        form_obj = CustomerForm(request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            if next_url:
                return redirect(next_url)
            return redirect(reverse('customer_list'))

        return render(request, 'crm/customer/customer.html', {'form_obj': form_obj}, )


'''用户编辑&添加
class Customer_edit(View):
    def get(self, request, id):
        edit_obj = models.Customer.objects.filter(id=id).first()
        if edit_obj:
            form_obj = CustomerForm(instance=edit_obj)
            return render(request, 'customer/customer_edit.html', {'form_obj': form_obj})

    def post(self, request, id):
        edit_obj = models.Customer.objects.filter(id=id).first()
        form_obj = CustomerForm(request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
        return render(request, 'customer/customer_edit.html', {'form_obj': form_obj})


class Customer_add(View):
    def get(self, request):
        form_obj = CustomerForm()
        return render(request, 'customer/customer_add.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = CustomerForm(request.POST)
        if form_obj.is_valid():
            print('校验成功')
            form_obj.save()
            return redirect(reverse('customer_list'))
        return render(request, 'customer/customer_add.html', {'form_obj': form_obj})

'''


# --> 客户展示视图
class Customer_list(View):
    def get(self, request, option_ret=None):

        q = self.get_search_contion(['qq', 'qq_name'])
        print(' -' * 10)
        print(q)
        if request.path_info == reverse('customer_list'):
            # --> 公户
            all_customer = models.Customer.objects.filter(
                q, consultant__isnull=True).order_by('-date')
            url = reverse('customer_list')
            title = '公户列表'

        else:
            # --> 私户my_customer
            all_customer = models.Customer.objects.filter(
                q, consultant=request.user).order_by('-date')
            url = reverse('my_customer_list')
            title = '私户列表'

        page_num = request.GET.get('page', 1)
        search_params = copy.deepcopy(request.GET)
        search_params._mutable = True  # --> 允许request.GET 可有修改, 在QueryDict源代码中可有找到相关的对应内容
        # from  django.http import QueryDict

        pagination_obj = Pagination(
            search_params, page_num=page_num, all_count=len(all_customer), url=url)

        # --> 生成一个QueryDict对象
        nextqd = QueryDict()
        nextqd._mutable = True  # --> QueryDict对象 可写
        nextqd['next'] = request.get_full_path()  # --> 获取当前页面的完整URl 放到nextqd中

        return render(request, 'crm/customer/customer_list.html', {
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
        if type(option_ret) == HttpResponse:
            return option_ret
        return self.get(request, option_ret=option_ret)

    def option_put_private(self):
        # --> 公户变私户
        request = self.request
        ids = request.POST.getlist('id')

        # --> 一对多正向操作
        # models.Customer.objects.filter(id__in=ids).update(consultant=request.user)

        # --> 一对多反向操作
        with transaction.atomic():
            add_list = models.Customer.objects.filter(
                id__in=ids, consultant__isnull=True).select_for_update()
            print('len(add_list)', len(add_list))
            print('len(ids)', len(ids))
            if len(ids) != len(add_list):
                return HttpResponse('123123213')
            request.user.customers.add(*add_list)
        return True

    def option_put_public(self):
        # --> 公户变私户
        request = self.request
        ids = request.POST.getlist('id')

        # --> 一对多正向操作
        # models.Customer.objects.filter(id__in=ids).update(consultant=None)

        # --> 一对多反向操作
        request.user.customers.remove(
            *models.Customer.objects.filter(id__in=ids))

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
