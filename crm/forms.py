from django import forms
from django.db.models import fields
from crm import models
from django.core.exceptions import ValidationError


# --> 基础Form类


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class StudyForm(BaseForm):
    class Meta:
        model = models.StudyRecord
        # fields = '__all__'
        exclude = ['homework', 'course_record', 'student']

# -->  班级记录Form
class CourseForm(BaseForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['has_homework'].widget.attrs.update({'class': ''})
        self.fields['teacher'].widget.choices = ((self.instance.teacher.id, self.instance.teacher),)

        re_class_choices = [(i.id, i) for i in self.instance.teacher.classlist.all()]
        self.fields['re_class'].widget.choices = re_class_choices


# --> 班级Form
class ClassForm(BaseForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    # def clean(self):
    #     ret = models.ClassList.objects.filter(
    #         course=self.cleaned_data.get('course'),
    #         semester=self.cleaned_data.get('semester'),
    #         campuses=self.cleaned_data.get('campuses'),
    #     )
    #     print('111111')
    #     print(self.cleaned_data.get('teachers'))
    #     if ret:
    #         self.add_error('course', '同一: 学期,校区,课程名称的班级已经存在,无法重复添加')
    #         raise ValidationError( '同一: 学期,校区,课程名称的班级已经存在,无法重复添加')
    #         # print(ret)
    #     return self.cleaned_data


# --> 跟进记录的form
class EnrollmentForm(BaseForm):
    class Meta:
        model = models.Enrollment
        exclude = ['delete_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract_agreed'].widget.attrs.update({'class': ''})
        self.fields['contract_approved'].widget.attrs.update({'class': ''})

        # print(self.fields['customer'])
        # print(self.instance)

        # --> 限制前端显示的customer(客户)数据, 只显示私户的,
        # print(self.instance)
        print(self.instance)
        choices = [(i.id, i)
                   for i in self.instance.customer.consultant.customers.all()]
        choices.insert(0, ('', '---------'))
        self.fields['customer'].widget.choices = choices

        # --> 限制前端显示的consultant(当前用户), 只显示自己
        # self.fields['consultant'].widget.choices = [(self.instance.consultant.id, self.instance.consultant)]


# --> 跟进记录的form
class ConsultRecordForm(BaseForm):
    class Meta:
        print('Meta执行')
        model = models.ConsultRecord
        exclude = ['delete_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('__init__执行')
        # print(self.fields['customer'])
        # print(self.instance)

        # --> 限制前端显示的customer(客户)数据, 只显示私户的,
        self.fields['customer'].widget.choices = [
            (i.id, i) for i in self.instance.consultant.customers.all()]
        print([(i.id, i) for i in self.instance.consultant.customers.all()])

        # --> 限制前端显示的consultant(当前用户), 只显示自己
        self.fields['consultant'].widget.choices = [
            (self.instance.consultant.id, self.instance.consultant)]


# --> 添加客户的form
class CustomerForm(BaseForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        widgets = {
            'course': forms.SelectMultiple
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs.update({'class': 'form-control'})


# --> 注册的form
class RegisterForm(BaseForm):
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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd != re_pwd:
            self.add_error('re_password', '两次密码不一致')
            raise ValidationError('两次密码不一致')
        return self.cleaned_data
