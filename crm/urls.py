from django.urls import path
from crm.views import customer
from crm.views import teacher

# --> 销售相关Url
urllist1 = [
    path('customer/', customer.Customer_list.as_view(), name='customer_list'),
    path('my_customer/', customer.Customer_list.as_view(), name='my_customer_list'),
    # path('customer/add', views.Customer_add.as_view(), name='customer_add'),
    # path('customer/edit/<int:id>', views.Customer_edit.as_view(), name='customer_edit'),
    path('customer/add/', customer.Customer.as_view(), name='customer_add'),
    path('customer/edit/<int:id>/',
         customer.Customer.as_view(), name='customer_edit'),
    # --> 展示跟进记录
    path('consult_record/list/', customer.ConsultRecord_list.as_view(),
         name='consult_record_list'),
    path('consult_record/add/', customer.ConsultRecord.as_view(),
         name='consult_record_add'),
    path('consult_record/edit/', customer.ConsultRecord.as_view(),
         name='consult_record_edit'),
    # path('consult_record/add/', views.ConsultRecord.as_view(), name='consult_record_add'),
    # path('consult_record/edit/<int:id>/', views.ConsultRecord.as_view(), name='consult_record_edit')
    # --> 报名记录
    path('enrollment/list/', customer.Enrollment_list.as_view(),
         name='enrollment_list'),
    path('enrollment/add/', customer.Enrollment.as_view(), name='enrollment_add'),
    path('enrollment/edit/', customer.Enrollment.as_view(), name='enrollment_edit'),
]

# --> 班主任相关URL
urllist2 = [
    path('class/list', teacher.ClassList.as_view(), name='class_list'),
    path('class/edit', teacher.Classes.as_view(), name='classes'),
    path('course/list', teacher.CourseList.as_view(), name='course_list'),
    path('course/edit', teacher.Courses.as_view(), name='course_edit'),
    path('study/list/<int:course_id>', teacher.StudyList.as_view(), name='study_list'),
    # path('study/edit/<', teacher.Study.as_view(), name='study_edit'),

]

# --> 合并路由
urlpatterns = urllist1 + urllist2
