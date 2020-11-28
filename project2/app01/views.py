import time

from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import redirect


def decoratorfunc(func):
    def warpper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        print('加载时间', time.time() - start)
        return ret

    return warpper


class Index(View):
    def get(self, request):
        data = {
            'name': 'Jerry',
            'age': 20,
        }
        return HttpResponse('This is Get Request')

        # return redirect('http://www.baidu.com')

#     def post(self, request):
#         return HttpResponse('This is Post Request')

#
# def index(request):
#     print(request)
#     return render(request, 'index.html')
