from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def Index(request):
    print('Index is Ok ')
    ret = HttpResponse('Index is Ok !')
    return  ret