from django import forms
from crm import models
from django.core.exceptions import ValidationError


#--> 添加客户的form
class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        widgets = {
            'course': forms.SelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# --> 注册的form
class RegisterForm(forms.ModelForm):
    re_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
        max_length=100,
        required=True
    )

    class Meta:
        model = models.UserProfile
        # fields =  '__all__'
        fields = ['username', 'password', 're_password', 'name', 'department']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput
        }
        labels = {
            'username': '用户名',
            'password': '密码',
            'name': '姓名',
            'department': '部门'
        }
        error_messages = {
            'password': {
                'required': '密码为必填!'

            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd != re_pwd:
            self.add_error('re_password', '两次密码不一致')
            raise ValidationError('两次密码不一致')
        return self.cleaned_data
