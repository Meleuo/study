from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout

# Create your views here.


def login_is_active(func):
    def wrapper(request, *args, **kwargs):
        cookie = request.session.get('login_demo')
        path_info = request.path_info
        if cookie != 'admin':
            return redirect('/login/?next=%s'%path_info)
        return func(request,  *args, **kwargs)
    return wrapper


class Login(View):

    @method_decorator(login_is_active)
    def get(self, request):
        print(request.path_info)
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.GET.get('next', None)
        if username == 'admin' and password == '123':
            ret = redirect('/home/')
            if next:
                ret = redirect(next)
            request.session['login_demo'] = 'admin'
            # ret.set_cookie('login_demo_cookie', 'admin', max_age=5)
            return ret
        return redirect('/login/')


@login_is_active
def home(request):
    return render(request, 'home.html')


class Index(View):
    @method_decorator(login_is_active)
    def get(self, request):
        return HttpResponse('Index is Ok')


def logout(request):
    request.session.flush()
    ret = redirect('/login/')
    # ret.delete_cookie('login_demo_cookie')
    return ret