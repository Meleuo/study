from django import forms
from django.core.validators import RegexValidator
from django.forms import ValidationError


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', required=True)
    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput)
    re_password = forms.CharField(label='重复密码', required=True, widget=forms.PasswordInput)

    # phone = forms.CharField(label='手机号')
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         print(self.fields[field].widget.attrs.update({'class': 'form-control '}))

    def clean(self):
        pwd_value = self.cleaned_data.get('password')
        re_pwd_value = self.cleaned_data.get('re_password')
        if pwd_value != re_pwd_value:
            self.add_error('re_password', '两次密码不想等')
            raise ValidationError('两次密码不想等')
        return self.cleaned_data

class Set_PwdFrom(forms.Form):
    old_passwd = forms.CharField(label='旧密码', required=True)
    new_passwd = forms.CharField(label='新密码', required=True)