from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib import auth
from demo_app.forms import RegForm, Set_PwdFrom
from django.contrib.auth.models import User
# from django.contrib.auth import lo
# Create your views here.



@login_required
def index(request):
    print(request.user)
    return render(request, 'index.html', {'user': request.user})

@login_required
def set_pwd(request):
    form_obj = Set_PwdFrom()
    msg = None
    if request.method == 'POST':
        form_obj = Set_PwdFrom(request.POST)
        if form_obj.is_valid():
            old_passwd = form_obj.cleaned_data.get('old_passwd')
            new_passwd = form_obj.cleaned_data.get('new_passwd')
            if request.user.check_password(old_passwd):
                request.user.set_password(new_passwd)
                request.user.save()
                msg = True
                print(msg)
            else:
                msg = False
                print(msg)
    return render(request, 'set_pwd.html', {'form_obj': form_obj, 'status': msg})

@login_required
def check_pwd(request):
    if request.is_ajax() and request.method == 'POST':
        value = request.POST.get('check_passwd')
        print(value)
        if request.user.check_password(value):
            return HttpResponse(0)
    return HttpResponse('error')

def logout(request):
    auth.logout(request)
    return redirect('/login/')


def register(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            username = form_obj.cleaned_data.get('user')
            password = form_obj.cleaned_data.get('pwd')
            print(username, password)
            form_obj.cleaned_data.pop('re_password')
            # request.POST.pop('re_pwd')
            User.objects.create_user(**form_obj.cleaned_data)
            return redirect('/login/')
    return  render(request, 'register.html', {'form_obj': form_obj})
    # return redirect('/login/')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = auth.authenticate(request, username=username, password=password)
        if obj:
            next_url = request.GET.get('next', None)
            auth.login(request, obj)
            if next_url:
                return redirect(next_url)
            return redirect('/index/')
    return render(request, 'login.html')