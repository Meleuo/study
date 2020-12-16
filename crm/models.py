# --> model 需要
from django.db import models
from multiselectfield import MultiSelectField, MultiSelectFormField

# --> 重写Auth 依赖
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib import auth
from django.utils.safestring import mark_safe

# --> 字段中的 choices

class_type_choices = (('fulltime', '脱产班',),
                      ('online', '网络班'),
                      ('weekend', '周末班',),)

course_choices = (('LinuxL', 'Linux中高级'),
                  ('PythonFullStack', 'Python高级全栈开发'),)

source_type_choices = (('qq', "qq群"),
                       ('referral', "内部转介绍"),
                       ('website', "官方网站"),
                       ('baidu_ads', "百度推广"),
                       ('office_direct', "直接上门"),
                       ('WoM', "口碑"),
                       ('public_class', "公开课"),
                       ('website_luffy', "路飞官网"),
                       ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

seek_status_choices = (('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'),)
pay_type_choices = (('deposit', "订金/报名费"),
                    ('tuition', "学费"),
                    ('transfer', "转班"),
                    ('dropout', "退学"),
                    ('refund', "退款"),)

attendance_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('absence', "缺勤"),
                      ('leave_early', "早退"),)

score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, ' D'),
                 (-1, 'N/A'),
                 (-100, 'COPY'),
                 (-1000, 'FAIL'),)


# --> 客户表
class Customer(models.Model):
    '''
    客户表
    '''
    qq = models.CharField(verbose_name='客户联系QQ',
                          max_length=11, unique=True, help_text='QQ必须是唯一')
    qq_name = models.CharField(
        verbose_name='QQ昵称', max_length=64, blank=True, null=True)
    name = models.CharField(verbose_name='客户名字', blank=True,
                            null=True, max_length=32, help_text='学员报名后, 请改为真实姓名')
    sex = models.CharField(verbose_name='客户性别', choices=(('male', '男'), ('female', '女')), max_length=10, default='male',
                           blank=True, null=True)
    birthday = models.DateField(
        verbose_name='出生日期', blank=True, null=True, help_text='格式: yyyy-mm-dd')
    phone = models.BigIntegerField(verbose_name='手机号', blank=True, null=True)
    source = models.CharField(verbose_name='客户来源', max_length=32, blank=True, null=True, choices=source_type_choices,
                              default='qq')
    introduce_from = models.ForeignKey(
        'Customer', verbose_name='自介绍', on_delete=models.CASCADE, blank=True, null=True)
    course = MultiSelectField(verbose_name='咨询的课程', choices=course_choices)
    class_type = models.CharField(
        verbose_name='班级类型', max_length=64, choices=class_type_choices, default='qq')
    customer_note = models.TextField(
        verbose_name="客户备注", blank=True, null=True, )
    status = models.CharField("状态", choices=enroll_status_choices, max_length=64, default="unregistered",
                              help_text="选择客户此时的状态")
    network_consult_note = models.TextField(
        blank=True, null=True, verbose_name='网络咨询师咨询内容')
    date = models.DateTimeField("咨询日期", auto_now_add=True)
    last_consult_date = models.DateTimeField("最后跟进日期", auto_now_add=True)
    next_date = models.DateTimeField("预计再次跟进时间", blank=True, null=True)
    network_consultant = models.ForeignKey('UserProfile', on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='网络咨询师',
                                           related_name='network_consultant')
    consultant = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name="销售", related_name='customers',
                                   blank=True, null=True, )
    class_list = models.ManyToManyField(
        'ClassList', verbose_name="已报班级", blank=True)

    class Meta:
        verbose_name = '客户列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.qq, self.name if self.name else self.qq_name)

    def show_class_list(self):
        msg = ''
        # for _class in self.class_list.all():
        #     msg = msg + str(_class)
        return ' | '.join([str(_class) for _class in self.class_list.all()])

    def show_status(self):
        '''
        (('signed', "已报名"),
                             ('unregistered', "未报名"),
                             ('studying', '学习中'),
                             ('paid_in_full', "学费已交齐"))
        '''
        status_color = {
            'signed': 'green',
            'unregistered': 'red',
            'studying': '#ffac00',
            'paid_in_full': 'blue'
        }
        return mark_safe(
            '<span style="height: 100%;padding: 3px;color: #fff;background-color: {}">{}</span>'.format(
                status_color[self.status], self.get_status_display())
        )


# --> 校区表
class Campuses(models.Model):
    """
    校区表
    """
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(
        verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '校区表'
        verbose_name_plural = verbose_name


# --> 合同模板表
class ContractTemplate(models.Model):
    """
    合同模板表
    """
    name = models.CharField("合同名称", max_length=128, unique=True)
    content = models.TextField("合同内容")
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '合同模板表'
        verbose_name_plural = verbose_name


# -->  班级表
class ClassList(models.Model):
    """
    班级表
    """
    course = models.CharField("课程名称", max_length=64, choices=course_choices)
    semester = models.IntegerField("学期")
    campuses = models.ForeignKey(
        'Campuses', on_delete=models.CASCADE, verbose_name="校区")
    price = models.IntegerField("学费", default=10000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField("结业日期", blank=True, null=True)
    contract = models.ForeignKey('ContractTemplate', on_delete=models.CASCADE, verbose_name="选择合同模版", blank=True,
                                 null=True)
    teachers = models.ManyToManyField('UserProfile', verbose_name="老师", related_name='classlist')
    class_type = models.CharField(choices=class_type_choices, max_length=64, verbose_name='班额及类型', blank=True,
                                  null=True)

    def __str__(self):
        return '第:%s期[%s]_(%s)' % (self.semester,self.get_course_display(), self.campuses.name)

    def show_teachers(self):
        return '|'.join([i.username for i in self.teachers.all()])

    class Meta:
        unique_together = ('course', 'semester', 'campuses')
        verbose_name = '班级表'
        verbose_name_plural = verbose_name


# --> 跟进记录表
class ConsultRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, verbose_name="所咨询客户")
    note = models.TextField(verbose_name="跟进内容...")
    status = models.CharField(
        "跟进状态", max_length=8, choices=seek_status_choices, help_text="选择客户此时的状态")
    consultant = models.ForeignKey(
        "UserProfile", on_delete=models.CASCADE, verbose_name="跟进人", related_name='records')
    date = models.DateTimeField("跟进日期", auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)


# --> 报名表
class Enrollment(models.Model):
    why_us = models.TextField("为什么报名", max_length=1024,
                              default=None, blank=True, null=True)
    your_expectation = models.TextField(
        "学完想达到的具体期望", max_length=1024, blank=True, null=True)
    contract_agreed = models.BooleanField(
        "我已认真阅读完培训协议并同意全部协议内容", default=False)
    contract_approved = models.BooleanField(
        "审批通过", help_text="在审阅完学员的资料无误后勾选此项,合同即生效", default=False)
    enrolled_date = models.DateTimeField(
        auto_now_add=True, verbose_name="报名日期")
    memo = models.TextField('备注', blank=True, null=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, verbose_name='客户名称')
    school = models.ForeignKey('Campuses', on_delete=models.CASCADE)
    enrolment_class = models.ForeignKey(
        "ClassList", on_delete=models.CASCADE, verbose_name="所报班级")

    class Meta:
        unique_together = ('enrolment_class', 'customer')


# --> 缴费记录
class PaymentRecord(models.Model):
    """
    缴费记录表
    """
    pay_type = models.CharField(
        "费用类型", choices=pay_type_choices, max_length=64, default="deposit")
    paid_fee = models.IntegerField("费用数额", default=0)
    note = models.TextField("备注", blank=True, null=True)
    date = models.DateTimeField("交款日期", auto_now_add=True)
    course = models.CharField("课程名", choices=course_choices,
                              max_length=64, blank=True, null=True, default='N/A')
    class_type = models.CharField(
        "班级类型", choices=class_type_choices, max_length=64, blank=True, null=True)
    enrolment_class = models.ForeignKey('ClassList', on_delete=models.CASCADE, verbose_name='所报班级', blank=True,
                                        null=True)
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, verbose_name="客户")
    consultant = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, verbose_name="销售")
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    status = models.BooleanField(verbose_name='审核', default=False)
    confirm_date = models.DateTimeField(
        verbose_name="确认日期", null=True, blank=True)
    confirm_user = models.ForeignKey('UserProfile', verbose_name="确认人",
                                     on_delete=models.CASCADE, related_name='confirms', null=True, blank=True)


# --> 课程记录表
class CourseRecord(models.Model):
    """课程记录表"""
    day_num = models.IntegerField("节次", help_text="此处填写第几节课或第几天课程...,必须为数字")
    date = models.DateField(auto_now_add=True, verbose_name="上课日期")
    course_title = models.CharField(
        '本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField(
        '本节课程内容', max_length=300, blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField(
        '本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField(
        '作业描述', max_length=500, blank=True, null=True)
    scoring_point = models.TextField(
        '得分点', max_length=300, blank=True, null=True)
    re_class = models.ForeignKey(
        'ClassList', on_delete=models.CASCADE, verbose_name="班级")
    teacher = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, verbose_name="班主任")

    def __str__(self):
        return '{course_title}[{day_num}]'.format(course_title=self.course_title, day_num=self.day_num)

    class Meta:
        unique_together = ('re_class', 'day_num')


# --> 学习记录
class StudyRecord(models.Model):
    """
    学习记录
    """
    attendance = models.CharField(
        "考勤", choices=attendance_choices, default="checked", max_length=64)
    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(
        max_length=255, verbose_name='作业批语', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField("备注", max_length=255, blank=True, null=True)
    homework = models.FileField(
        verbose_name='作业文件', blank=True, null=True, default=None)
    course_record = models.ForeignKey(
        'CourseRecord', on_delete=models.CASCADE, verbose_name="某节课程")
    student = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, verbose_name="学员")


# --> 部门表
class Department(models.Model):
    name = models.CharField(verbose_name='部门名称', max_length=32)
    count = models.IntegerField(verbose_name='部门人数', default=0)

    def __str__(self):
        return self.name


# --> 后台用户表 objects 方法对象
class UserManager(BaseUserManager):
    '''
    Django auth objects的方法, 取自源码, 改写一部分
    '''
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        项目中设计的 username 即为email, 原来的email相关的内容就不再需要了
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


# --> 后台用户表
class UserProfile(AbstractBaseUser, PermissionsMixin):
    '''
    基础后台用户表, 继承Django内置User auth的基类
    '''
    username = models.EmailField(
        verbose_name='后台用户名/email', max_length=200, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    # --> 改写一部分内容
    name = models.CharField(verbose_name='名字', max_length=10)
    is_admin = models.BooleanField(default=False)
    department = models.ForeignKey(Department, verbose_name='所属部门', on_delete=models.CASCADE, default=None,
                                   blank=True,
                                   null=True)
    mobile = models.CharField(
        verbose_name='手机号', max_length=11, default=None, blank=True, null=True)
    memo = models.TextField(verbose_name='备注', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = '账户信息'
        verbose_name_plural = verbose_name

    def clean(self):
        super().clean()
        self.username = self.__class__.objects.normalize_email(self.username)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.username, self.username)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.username], **kwargs)
