import os
import sys
import random

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM_Pro.settings')
    import django
    from  django.db.models import Q
    django.setup()
    from crm import models
    ret = models.ClassList.objects.filter(Q(course__contains='L'))
    print(ret)

    # _class = models.ClassList.objects.first()
    # # print(_class)
    #
    # class_type_choices = (('fulltime', '脱产班',),
    #                       ('online', '网络班'),
    #                       ('weekend', '周末班',),)
    #
    # course_choices = (('LinuxL', 'Linux中高级'),
    #                   ('PythonFullStack', 'Python高级全栈开发'),)
    #
    # source_type_choices = (('qq', "qq群"),
    #                        ('referral', "内部转介绍"),
    #                        ('website', "官方网站"),
    #                        ('baidu_ads', "百度推广"),
    #                        ('office_direct', "直接上门"),
    #                        ('WoM', "口碑"),
    #                        ('public_class', "公开课"),
    #                        ('website_luffy', "路飞官网"),
    #                        ('others', "其它"),)
    #
    # enroll_status_choices = (('signed', "已报名"),
    #                          ('unregistered', "未报名"),
    #                          ('studying', '学习中'),
    #                          ('paid_in_full', "学费已交齐"))
    # print()
    #
    # xs = models.UserProfile.objects.first()
    #
    # def create_test_db():
    #     qq_num = 20000 + 5
    #     qq_name_str = 6 + 5
    #     for i in range(300):
    #         obj = models.Customer.objects.create(qq=qq_num, qq_name='建国同志%s号' % qq_name_str,
    #                                              class_type=class_type_choices[random.randint(0, len(class_type_choices) - 1)][0],
    #                                              status=enroll_status_choices[random.randint(0, len(enroll_status_choices) - 1)][0],
    #                                              course=course_choices[random.randint(0, len(course_choices) - 1)][0],
    #                                              consultant=xs,
    #                                              source=source_type_choices[random.randint(0, len(source_type_choices) - 1)][0],
    #                                              )
    #         obj.class_list.add(_class)
    #         qq_num += 1
    #         qq_name_str += 1
    #
    # create_test_db()