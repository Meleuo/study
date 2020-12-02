from django.shortcuts import render, redirect
from django.views.generic import View
from register.forms import RegisterForm
from register.forms import RegForm


class RegView(View):
    # TEMPLATE = 'reg.html'

    def get(self, request):
        form_obj = RegForm()
        return render(request, 'reg.html', {'form_obj': form_obj})

    def post(self, request):
        pass


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'reg.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            print('校验成功')
            print(register_form.cleaned_data.get('user'))
            print(register_form.errors)

        else:
            print('校验失败')
            return render(request, 'reg.html', {'register_form': register_form})
        return redirect('/index/')
