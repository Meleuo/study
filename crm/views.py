from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.utils.safestring import mark_safe
from django.contrib import auth

from crm import models
from crm.forms import RegisterForm
from crm import models
from utils.pagination import Pagination


class Customer_list(View):
    def get(self, request):
        all_customer = models.Customer.objects.all()
        page_num = request.GET.get('page', 1)

        pagination_obj = Pagination(page_num=page_num, len_customer=len(all_customer), url=reverse('customer_list'))

        return render(request, 'crm/customer_list.html', {
            'all_customer': all_customer[pagination_obj.start:pagination_obj.end],
            'html_page': mark_safe(pagination_obj.show_html)
        })


# class Customer_list(View):
#
#     def get(self, request):
#         page_num = request.GET.get('page', 1)
#         try:
#             page_num = int(page_num)
#             if page_num <= 0:
#                 page_num = 1
#         except Exception as e:
#             page_num = 1
#
#         per_num = 10  # --> 一页显示数据条数
#         start_num = (page_num - 1) * per_num
#         stop_num = page_num * per_num
#
#         # --> 获取页数
#         all_customer = models.Customer.objects.all()
#         all_count, more = divmod(len(all_customer), per_num)
#         if more:
#             all_count = all_count + 1
#
#         max_show = 10  # --> 最多显示的页码数
#         half_show = max_show // 2  # --> 取得两边分页的长度, // 向下取值
#
#         if page_num <= half_show:  # -->  倘若请求的页面小于2边分页的长度
#             page_start = 1  # --> 分页起始值写死为1
#             page_end = max_show + 1  # --> 分页结束值设置为最大值, 再加上当前页面的分页, 一共是11个分页
#         elif page_num >= all_count - half_show:  # --> 倘若请求的页面大于  (全部页面数 - 分页数)
#             page_start = all_count - max_show  # --> 起始页面 设置为 页面总数 - 最大长度
#             page_end = all_count  # --> 结尾设置总数即可
#         else:  # --> 其他正常情况保证当前分页的两侧有对应的数量的分页即可
#             page_start = page_num - half_show
#             page_end = page_num + half_show
#
#         # --> 生成HTML
#         html_page = ''
#         if page_num > 1:
#             html_page = '<li><a href="{url}?page=1" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>' \
#                         '<li><a href="{url}?page={count}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' \
#                 .format(url=reverse('customer_list'), count=page_num - 1)
#         else:
#             html_page += '<li class="disabled"><span aria-hidden="true">首页</span></li><li class="disabled"><span aria-hidden="true">&laquo;</span></li>'
#
#
#         for count in range(page_start, page_end + 1):
#             page_is_active = ''
#             if page_num == count:
#                 page_is_active = 'class="active"'
#             html_page += '<li {active}><a href="{url}?page={count}">{count}</a></li>' \
#                 .format(active=page_is_active, url=reverse('customer_list'), count=count)
#
#         if page_num < all_count:
#             html_page += '<li><a href="{url}?page={count}" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>' \
#                          '<li><a href="{url}?page={all_count}" aria-label="Previous"><span aria-hidden="true">尾页</span></a></li>' \
#                 .format(url=reverse('customer_list'), count=page_num + 1, all_count=all_count)
#         else:
#             html_page += '<li class="disabled"><span aria-hidden="true">&raquo;</span></li><li class="disabled"><span aria-hidden="true">尾页</span></li>'
#
#         return render(request, 'crm/customer_list.html', {
#             'all_customer': all_customer[start_num:stop_num],
#             'html_page': mark_safe(html_page)
#         })


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
