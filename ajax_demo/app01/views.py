from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
# Create your views here.

class Index(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return render(request, 'index.html')


class CView(View):
    def post(self, request):
        msg = request.POST.get('msg')
        dmsg = json.loads(msg)
        print(dmsg)
        dmsg['server'] = 'Yes'
        res_msg = json.dumps(dmsg)
        return HttpResponse(res_msg)

def upload(request):
    if request.is_ajax():
        my_file = request.FILES.get('f1')
        with open(my_file.name, 'wb') as f:
            for i in my_file.chunks():
                f.write(i)
        return HttpResponse('Yes')
    return render(request, 'upload.html')