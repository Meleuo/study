from django.urls import path
from crm import views

urlpatterns = [
    path('customer_list', views.Customer_list.as_view(), name='customer_list')
]
