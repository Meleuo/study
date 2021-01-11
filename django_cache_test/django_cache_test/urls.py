"""django_cache_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import time
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

from django.views.decorators.cache import cache_page  # --> 视图绑定缓存的语法糖


@cache_page(5)  # --> 第一个参数为缓存的时间
def test_view(request):
    return render(request, 'test.html', {
        'time': time.time()
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_view),
    # path('test/', cache_page(5)(test_view))  # --> 为视图绑定缓存也可以在URL上面绑定

]
