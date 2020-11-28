from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from book_os.models import User, Book
from book_os.models import Book as Book_DB
from book_os.models import Press as Press_DB




# Create your views here.

class Login(View):
    def get(self, request):
        error = request.GET.get('error', False)
        return render(request, 'login.html', {'error': error})

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        ret = User.objects.filter(username=username, password=password)
        if ret:
            return redirect(reverse('index'))
        return redirect(reverse('login') + '?error=登录失败')


class Index(View):
    def get(self, request):
        return render(request, 'index.html', {'index': True})


class Book(View):
    def get(self, request, operation):
        if operation == 'list':
            book_db_obj = Book_DB.objects.all()
            return render(request, 'book.html', {'book': True, 'book_db_obj': book_db_obj})
        return render(request, 'index.html')

class Press(View):
    def get(self, request, operation):
        if operation == 'list':
            press_db_obj = Press_DB.objects.all()
            print(press_db_obj[0].book.all())
            return render(request, 'press.html', {'press': True, 'press_db_obj': press_db_obj})
        return render(request, 'index.html')