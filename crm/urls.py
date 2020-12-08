from django.urls import path
from crm import views

urlpatterns = [
    path('customer/', views.Customer_list.as_view(), name='customer_list'),
    path('my_customer/', views.Customer_list.as_view(), name='my_customer_list'),
    # path('customer/add', views.Customer_add.as_view(), name='customer_add'),
    # path('customer/edit/<int:id>', views.Customer_edit.as_view(), name='customer_edit'),
    path('customer/add/', views.Customer.as_view(), name='customer_add'),
    path('customer/edit/<int:id>/', views.Customer.as_view(), name='customer_edit'),

]
