from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


class Md1(MiddlewareMixin):
    def process_request(self, request):
        ret = HttpResponse('Md1 process_request is OK!')
        print('md1 process_request')
        # return ret

    def process_response(self, request, response):
        print('md1 process_response')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('Md1 process_view')
        print(view_func, view_args, view_kwargs)
        # ret = HttpResponse('Md1 process_view is OK!')
        # return ret

    def process_exception(self,  request, exception):
        print('Md1 process_exception')
        print(exception)

    def process_template_response(self, request, response):
        print(response)
        print('Md1 process_template_response')
        return response



class Md2(MiddlewareMixin):
    def process_request(self, request):
        ret = HttpResponse('Md2 process_request is OK!')
        print('md2 process_request')
        # return ret


    def process_response(self, request, response):
        print('md2 process_response')
        return response


    def process_view(self, request, view_func, view_args, view_kwargs):
        print('Md2 process_view')
        print(view_func, view_args, view_kwargs)
        # ret = HttpResponse('Md2 process_view is OK!')
        # return ret

    def process_exception(self, request, exception):
        print('Md2 process_exception')
        print(exception)
        ret = HttpResponse('Md2 process_exception is OK!')
        return ret

    def process_template_response(self, request, response):
        print(response)
        print('Md2 process_template_response')
        return response
