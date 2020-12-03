import re
from django import forms
from django.core.validators import RegexValidator
from django.forms import ValidationError


class RegForm(forms.Form):
    user = forms.CharField(label='用户名', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pwd = forms.CharField(label='密码', required=True, widget=forms.PasswordInput)
    re_pwd = forms.CharField(label='重复密码', required=True, widget=forms.PasswordInput)
    # phone = forms.CharField(label='手机号')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(self.fields[field].widget.attrs.update({'class': 'form-control '}))

    def clean(self):
        pwd_value = self.cleaned_data.get('pwd')
        re_pwd_value = self.cleaned_data.get('re_pwd')
        if pwd_value != re_pwd_value:
            self.add_error('re_pwd', '两次密码不想等')
            raise ValidationError('两次密码不想等')
        return self.cleaned_data

def phone_check(value):
    if not re.match(r'^1[3-9]\d{9}$', value):
        raise ValidationError('手机号不符合规则')


class RegisterForm(forms.Form):
    user = forms.CharField(label='用户名', required=True, min_length=5)
    pwd = forms.CharField(label='密码', required=True, widget=forms.PasswordInput)
    re_pwd = forms.CharField(label='重复密码', required=True, widget=forms.PasswordInput)

    def clean(self):
        pwd_value = self.cleaned_data.get('pwd')
        re_pwd_value = self.cleaned_data.get('re_pwd')
        if pwd_value != re_pwd_value:
            self.add_error('re_pwd', '两次密码不想等')
            raise ValidationError('两次密码不想等')
        return self.cleaned_data
    # def clean_pwd(self):
    #     pwd_value = self.cleaned_data.get('pwd')
    #     if not len(pwd_value) < 3:
    #         return pwd_value
    #     raise  ValidationError('你太短了')
    # is18 = forms.BooleanField(label='是否成年')
    # hobby = forms.MultipleChoiceField(label='爱好',
    #                           widget=forms.SelectMultiple,
    #                           choices=(
    #                               (1, '吃饭'),
    #                               (2, '睡觉'),
    #                               (3, '打豆豆')), )
    # phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3-9]\d{9}', '手机号不符合规则')])
    # phone = forms.CharField(label='手机号', validators=[phone_check, ])
    # sex = forms.ChoiceField(widget=forms.SelectMultiple )
