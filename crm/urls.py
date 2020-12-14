from django.urls import path
from crm.views import customer

urlpatterns = [
    path('customer/', customer.Customer_list.as_view(), name='customer_list'),
    path('my_customer/', customer.Customer_list.as_view(), name='my_customer_list'),
    # path('customer/add', views.Customer_add.as_view(), name='customer_add'),
    # path('customer/edit/<int:id>', views.Customer_edit.as_view(), name='customer_edit'),
    path('customer/add/', customer.Customer.as_view(), name='customer_add'),
    path('customer/edit/<int:id>/', customer.Customer.as_view(), name='customer_edit'),
    # --> 展示跟进记录
    path('consult_record/list/', customer.ConsultRecord_list.as_view(), name='consult_record_list'),
    path('consult_record/add/', customer.ConsultRecord.as_view(), name='consult_record_add'),
    path('consult_record/edit/', customer.ConsultRecord.as_view(), name='consult_record_edit'),
    # path('consult_record/add/', views.ConsultRecord.as_view(), name='consult_record_add'),
    # path('consult_record/edit/<int:id>/', views.ConsultRecord.as_view(), name='consult_record_edit')

    #--> 报名记录
    path('enrollment/list/', customer.Enrollment_list.as_view(), name='enrollment_list'),
    path('enrollment/add/', customer.Enrollment.as_view(), name='enrollment_add'),
    path('enrollment/edit/', customer.Enrollment.as_view(), name='enrollment_edit'),

]
