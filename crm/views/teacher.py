# --> 班主任操作试图
import copy
import time

from django.views.generic import View
from django.shortcuts import render, reverse, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.http import QueryDict

from utils.pagination import Pagination
from crm import models
from crm import forms


class Courses(View):
    def get(self, request):
        form_obj = forms.CourseForm()
        return render(request, 'crm/teacher/courses.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = forms.CourseForm(request.POST)
        if form_obj.is_valid:
            form_obj.save()
            return redirect(reverse('course_list'))
        return render(request, 'crm/teacher/courses.html', {'form_obj': form_obj})


class CourseList(View):
    def get(self, request):
        all_course = models.CourseRecord.objects.all()
        add_btn_html = self.add_button()
        return render(request, 'crm/teacher/course_list.html', {'all_course': all_course, 'add_btn_html': add_btn_html})

    def add_button(self):
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = self.request.get_full_path()
        btn_url = '%s?%s' % (reverse('course_edit'), qd.urlencode())
        btn = '<a class="btn-success btn" style="margin-bottom: 5px"href="{url}">添加记录</a>'.format(
            url=btn_url)
        return mark_safe(btn)


class Classes(View):
    def get(self, request):
        form_obj = forms.ClassForm()
        return render(request, 'crm/teacher/classes.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = forms.ClassForm(request.POST)
        next_url = request.GET.get('next', None)
        if form_obj.is_valid():
            form_obj.save()
            if next_url:
                return redirect(next_url)
            return redirect(reverse('class_list'))
        return render(request, 'crm/teacher/classes.html', {'form_obj': form_obj})


class ClassList(View):
    def get(self, request):
        # --> 搜索实现
        all_classs = models.ClassList.objects.filter(
            self.get_search_contion(['course']))

        # --> 分页

        page_num = request.GET.get('page_num', 1)
        search_params = copy.deepcopy(request.GET)
        search_params._mutable = True
        page = Pagination(search_params=search_params, page_num=page_num, all_count=len(all_classs),
                          url=reverse('class_list'))

        return render(request, 'crm/teacher/class_list.html',
                      {'all_classs': all_classs[page.start:page.end],
                       'page_html': mark_safe(page.show_html),
                       'add_btn_html': self.add_button()})

    def add_button(self):
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = self.request.get_full_path()
        btn_url = '%s?%s' % (reverse('classes'), qd.urlencode())
        btn = '<a class="btn-success btn" style="margin-bottom: 5px"href="{url}">添加记录</a>'.format(
            url=btn_url)
        return mark_safe(btn)

    def get_search_contion(self, contions=['course']):
        search = self.request.GET.get('search', '')
        for contion in contions:
            q = Q()
            q.connector = 'OR'
            q.children.append(Q(('%s__contains' % contion, search)))
        return q

    # def post(self, request):
