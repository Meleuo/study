# Generated by Django 3.1.4 on 2020-12-06 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='校区')),
                ('address', models.CharField(blank=True, max_length=512, null=True, verbose_name='详细地址')),
            ],
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[('LinuxL', 'Linux中高级'), ('PythonFullStack', 'Python高级全栈开发')], max_length=64, verbose_name='课程名称')),
                ('semester', models.IntegerField(verbose_name='学期')),
                ('price', models.IntegerField(default=10000, verbose_name='学费')),
                ('memo', models.CharField(blank=True, max_length=100, null=True, verbose_name='说明')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('graduate_date', models.DateField(blank=True, null=True, verbose_name='结业日期')),
                ('class_type', models.CharField(blank=True, choices=[('fulltime', '脱产班'), ('online', '网络班'), ('weekend', '周末班')], max_length=64, null=True, verbose_name='班额及类型')),
                ('campuses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.campuses', verbose_name='校区')),
            ],
        ),
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='合同名称')),
                ('content', models.TextField(verbose_name='合同内容')),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.IntegerField(help_text='此处填写第几节课或第几天课程...,必须为数字', verbose_name='节次')),
                ('date', models.DateField(auto_now_add=True, verbose_name='上课日期')),
                ('course_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节课程标题')),
                ('course_memo', models.TextField(blank=True, max_length=300, null=True, verbose_name='本节课程内容')),
                ('has_homework', models.BooleanField(default=True, verbose_name='本节有作业')),
                ('homework_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节作业标题')),
                ('homework_memo', models.TextField(blank=True, max_length=500, null=True, verbose_name='作业描述')),
                ('scoring_point', models.TextField(blank=True, max_length=300, null=True, verbose_name='得分点')),
                ('re_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.classlist', verbose_name='班级')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='讲师')),
            ],
            options={
                'unique_together': {('re_class', 'day_num')},
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qq', models.CharField(help_text='QQ必须是唯一', max_length=11, unique=True, verbose_name='客户联系QQ')),
                ('qq_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='QQ昵称')),
                ('name', models.CharField(blank=True, help_text='学员报名后, 请改为真实姓名', max_length=32, null=True, verbose_name='客户名字')),
                ('sex', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], default='male', max_length=10, null=True, verbose_name='客户性别')),
                ('birthday', models.DateField(blank=True, help_text='格式: yyyy-mm-dd', null=True, verbose_name='出生日期')),
                ('phone', models.BigIntegerField(blank=True, null=True, verbose_name='手机号')),
                ('source', models.CharField(blank=True, choices=[('qq', 'qq群'), ('referral', '内部转介绍'), ('website', '官方网站'), ('baidu_ads', '百度推广'), ('office_direct', '直接上门'), ('WoM', '口碑'), ('public_class', '公开课'), ('website_luffy', '路飞官网'), ('others', '其它')], default='qq', max_length=32, null=True, verbose_name='客户来源')),
                ('course', multiselectfield.db.fields.MultiSelectField(choices=[('LinuxL', 'Linux中高级'), ('PythonFullStack', 'Python高级全栈开发')], max_length=22, verbose_name='咨询的课程')),
                ('class_type', models.CharField(choices=[('qq', 'qq群'), ('referral', '内部转介绍'), ('website', '官方网站'), ('baidu_ads', '百度推广'), ('office_direct', '直接上门'), ('WoM', '口碑'), ('public_class', '公开课'), ('website_luffy', '路飞官网'), ('others', '其它')], default='qq', max_length=64, verbose_name='班级类型')),
                ('customer_note', models.TextField(blank=True, null=True, verbose_name='客户备注')),
                ('status', models.CharField(choices=[('signed', '已报名'), ('unregistered', '未报名'), ('studying', '学习中'), ('paid_in_full', '学费已交齐')], default='unregistered', help_text='选择客户此时的状态', max_length=64, verbose_name='状态')),
                ('network_consult_note', models.TextField(blank=True, null=True, verbose_name='网络咨询师咨询内容')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='咨询日期')),
                ('last_consult_date', models.DateField(auto_now_add=True, verbose_name='最后跟进日期')),
                ('next_date', models.DateField(blank=True, null=True, verbose_name='预计再次跟进时间')),
                ('class_list', models.ManyToManyField(to='crm.ClassList', verbose_name='已报班级')),
                ('consultant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL, verbose_name='销售')),
                ('introduce_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='自介绍')),
                ('network_consultant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='network_consultant', to=settings.AUTH_USER_MODEL, verbose_name='网络咨询师')),
            ],
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.CharField(choices=[('checked', '已签到'), ('vacate', '请假'), ('late', '迟到'), ('absence', '缺勤'), ('leave_early', '早退')], default='checked', max_length=64, verbose_name='考勤')),
                ('score', models.IntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'C+'), (50, 'C'), (40, 'C-'), (0, ' D'), (-1, 'N/A'), (-100, 'COPY'), (-1000, 'FAIL')], default=-1, verbose_name='本节成绩')),
                ('homework_note', models.CharField(blank=True, max_length=255, null=True, verbose_name='作业批语')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('homework', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='作业文件')),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.courserecord', verbose_name='某节课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='学员')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_type', models.CharField(choices=[('deposit', '订金/报名费'), ('tuition', '学费'), ('transfer', '转班'), ('dropout', '退学'), ('refund', '退款')], default='deposit', max_length=64, verbose_name='费用类型')),
                ('paid_fee', models.IntegerField(default=0, verbose_name='费用数额')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='交款日期')),
                ('course', models.CharField(blank=True, choices=[('LinuxL', 'Linux中高级'), ('PythonFullStack', 'Python高级全栈开发')], default='N/A', max_length=64, null=True, verbose_name='课程名')),
                ('class_type', models.CharField(blank=True, choices=[('fulltime', '脱产班'), ('online', '网络班'), ('weekend', '周末班')], max_length=64, null=True, verbose_name='班级类型')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('status', models.BooleanField(default=False, verbose_name='审核')),
                ('confirm_date', models.DateTimeField(blank=True, null=True, verbose_name='确认日期')),
                ('confirm_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='confirms', to=settings.AUTH_USER_MODEL, verbose_name='确认人')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='销售')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='客户')),
                ('enrolment_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.classlist', verbose_name='所报班级')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='跟进内容...')),
                ('status', models.CharField(choices=[('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'), ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效')], help_text='选择客户此时的状态', max_length=8, verbose_name='跟进状态')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='跟进日期')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL, verbose_name='跟进人')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='所咨询客户')),
            ],
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.contracttemplate', verbose_name='选择合同模版'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='老师'),
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('why_us', models.TextField(blank=True, default=None, max_length=1024, null=True, verbose_name='为什么报名')),
                ('your_expectation', models.TextField(blank=True, max_length=1024, null=True, verbose_name='学完想达到的具体期望')),
                ('contract_agreed', models.BooleanField(default=False, verbose_name='我已认真阅读完培训协议并同意全部协议内容')),
                ('contract_approved', models.BooleanField(default=False, help_text='在审阅完学员的资料无误后勾选此项,合同即生效', verbose_name='审批通过')),
                ('enrolled_date', models.DateTimeField(auto_now_add=True, verbose_name='报名日期')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customer', verbose_name='客户名称')),
                ('enrolment_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.classlist', verbose_name='所报班级')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.campuses')),
            ],
            options={
                'unique_together': {('enrolment_class', 'customer')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together={('course', 'semester', 'campuses')},
        ),
    ]