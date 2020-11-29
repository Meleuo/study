from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def Index(request):
    print('Index is Ok ')
    ret = HttpResponse('Index is Ok !')
    def __render():
        print('render Is OK!')
        return HttpResponse('render Is OK!')
    ret.render = __render
    return  ret