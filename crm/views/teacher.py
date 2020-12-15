# --> 班主任操作试图
import copy
# import time

from django.views.generic import View
from django.shortcuts import render, reverse, redirect
from django.db.models import Q
from django.utils.safestring import mark_safe
# from django.http import HttpResponse
from django.http import QueryDict

from utils.pagination import Pagination
from crm import models
from crm import forms


class Courses(View):
    def get(self, request):
        title, form_obj = self.get_title_form_obj()
        # form_obj = forms.CourseForm(instance=models.CourseRecord(teacher=request.user))
        return render(request, 'form.html', {'form_obj': form_obj, 'title': title})

    def post(self, request):
        title, form_obj = self.get_title_form_obj(method=request.POST)
        next_url = request.GET.get('next', None)

        # form_obj = forms.CourseForm(request.POST, instance=models.CourseRecord(teacher=request.user))
        if form_obj.is_valid():
            form_obj.save()
            if next_url:
                return redirect(next_url)
            return redirect(reverse('course_list'))
        return render(request, 'form.html', {'form_obj': form_obj, 'title': title})

    def get_title_form_obj(self, method=None):
        request = self.request
        course_edit_id = request.GET.get('course_edit_id', None)
        if course_edit_id and course_edit_id.isdigit():
            title = '修改课程记录'
            form_obj = forms.CourseForm(method,
                                        instance=models.CourseRecord.objects.filter(id=int(course_edit_id)).first())
        else:
            title = '添加课程记录'
            form_obj = forms.CourseForm(method,
                                        instance=models.CourseRecord(teacher=request.user))
        return title, form_obj


class CourseList(View):
    def get(self, request):

        # --> 搜索实现
        q = self.get_search_contion(contions=['course_title', 'course_memo', 'homework_title', 'homework_memo'])
        class_id = request.GET.get('class_id', None)
        if class_id:
            all_course = models.CourseRecord.objects.filter(q,
                                                            teacher=request.user,
                                                            re_class_id=int(class_id)
                                                            )
        else:
            all_course = models.CourseRecord.objects.filter(q, teacher=request.user)

        # --> 分页
        search_params = copy.deepcopy(request.GET)
        search_params._mutable = True
        page_num = request.GET.get('page', 1)
        page = Pagination(search_params=search_params, page_num=page_num, all_count=len(all_course),
                          url=reverse('course_list'),
                          per_num=2)

        add_btn_html = self.add_button()
        return render(request, 'crm/teacher/course_list.html', {
            'all_course': all_course[page.start:page.end],
            'add_btn_html': add_btn_html,
            'title': '课程记录',
            'page_html': mark_safe(page.show_html)
        })

    def add_button(self):
        qd = QueryDict()
        qd._mutable = True
        qd['next'] = self.request.get_full_path()
        btn_url = '%s?%s' % (reverse('course_edit'), qd.urlencode())
        btn = '<a class="btn-success btn" style="margin-bottom: 5px"href="{url}">添加记录</a>'.format(
            url=btn_url)
        return mark_safe(btn)

    def get_search_contion(self, contions=['course_title']):
        search = self.request.GET.get('search', '')
        q = Q()
        q.connector = 'OR'
        for contion in contions:
            q.children.append(Q(('%s__contains' % contion, search), ))
        return q


class Classes(View):
    def get(self, request):
        title, form_obj = self.get_title_form_obj()
        print(123)
        return render(request, 'form.html', {'form_obj': form_obj, 'title': title})

    def post(self, request):
        title, form_obj = self.get_title_form_obj(method=request.POST)
        next_url = request.GET.get('next', None)
        if form_obj.is_valid():
            form_obj.save()
            if next_url:
                return redirect(next_url)
            return redirect(reverse('class_list'))
        return render(request, 'form.html', {'form_obj': form_obj, 'title': title})

    def get_title_form_obj(self, method=None):
        request = self.request
        edit_classe_id = request.GET.get('edit_classe_id', None)
        if edit_classe_id and edit_classe_id.isdigit():
            title = '修改班级'
            form_obj = forms.ClassForm(method, instance=models.ClassList.objects.filter(id=int(edit_classe_id)).first())
        else:
            title = '添加班级'
            form_obj = forms.ClassForm(method)
        return title, form_obj


class ClassList(View):
    def get(self, request):
        # --> 搜索实现
        all_classs = models.ClassList.objects.filter(
            self.get_search_contion(['course']))

        # --> 分页

        page_num = request.GET.get('page', 1)
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

    def get_search_contion(self, contions=None):
        global q
        if contions is None:
            contions = ['course']
        search = self.request.GET.get('search', '')
        for contion in contions:
            q = Q()
            q.connector = 'OR'
            q.children.append(Q(('%s__contains' % contion, search)))
        return q

    # def post(self, request):
