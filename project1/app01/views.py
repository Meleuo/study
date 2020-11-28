# coding: utf-8
import os

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from app01.models import User
from app01.models import Press
from app01.models import Book
from app01.models import BookFile
from app01.models import Author
from project1.settings import BASE_DIR
from django.views.generic import View


def index(request):
    return render(request, 'index.html')


def login(request):
    msg = ''
    if request.method == 'POST':
        print(request.method)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        ret = User.objects.filter(username=username, password=password)
        if ret:
            return redirect('/index/')
        msg = '登录失败'

    return render(request, 'login.html', {
        'error': msg
    })


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        print(request.method)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        ret = User.objects.filter(username=username, password=password)
        if ret:
            return redirect('/index/')
        return render(request, 'login.html', {'error': '登录失败'})


def press_list(request):
    press_all = Press.objects.all()
    return render(request, 'press_list.html', {'ret': press_all})


def add_press(request):
    msg = ''
    if request.method == 'POST':
        press_name = request.POST.get('press_name', '')
        if press_name:
            Press.objects.create(name=press_name)
            return redirect('/press_list/')

    return render(request, 'add_press.html', {'msg': msg})


def delete_press(request):
    press_id = request.GET.get('id', None)
    if press_id:
        Press.objects.filter(id=press_id).delete()
        print(press_id)
    return redirect('/press_list/')


def edit_press(request):
    press_id = request.GET.get('id', None)
    if request.method == 'POST':
        # press_id = request.GET.get('press_id')
        new_press_name = request.POST.get('press_name')
        ret_press = Press.objects.filter(id=press_id)[0]
        ret_press.name = new_press_name
        ret_press.save()
        return redirect('/press_list/')

    press_id = request.GET.get('id', None)
    ret_press = Press.objects.filter(id=press_id)
    return render(request, 'edit_press.html', {'press_obj': ret_press[0]})


def book_list(request):
    books_obj = Book.objects.all()
    return render(request, 'book_list.html', {'books_obj': books_obj})


def add_book(request):
    press_list_obj = Press.objects.all()
    if request.method == 'POST':
        book_title = request.POST.get('book_title', None)
        press_id = request.POST.get('press_id', None)
        Book.objects.create(title=book_title, press_id=press_id)
        return redirect('/book_list/')

    return render(request, 'add_book.html', {'press_list_obj': press_list_obj})


def delete_book(request):
    id = request.GET.get('id', None)
    if id:
        Book.objects.filter(id=id)[0].delete()
    return render(request, 'delete_book.html')


def edit_book(request):
    id = request.GET.get('id', None)
    if request.method == 'POST':
        new_press_id = request.POST.get('new_press_id')
        new_book_title = request.POST.get('new_book_title')
        edit_book_obj = Book.objects.get(id=id)
        edit_book_obj.title = new_book_title
        edit_book_obj.press_id = new_press_id
        edit_book_obj.save()
        return redirect('/book_list/')

    book_obj = Book.objects.filter(id=id)[0]
    press_obj = Press.objects.all()
    return render(request, 'edit_book.html', {'book_obj': book_obj, 'press_obj': press_obj})


def author_list(request):
    author_list_obj = Author.objects.all()
    print(author_list_obj[0].books.all()[0].title)
    return render(request, 'author_list.html', {
        'author_list_obj': author_list_obj
    })


def add_author(request):
    book_list_obj = Book.objects.all()
    if request.method == 'POST':
        books_id = request.POST.getlist('books')
        author = request.POST.get('author')
        new_author = Author.objects.create(author=author)
        # for book_id in books_id:
        new_author.books.add(*books_id)
        return redirect('/author_list/')
    return render(request, 'add_author.html', {'book_list_obj': book_list_obj})


def delete_author(request):
    id = request.GET.get('id')
    Author.objects.get(id=id).delete()
    return redirect('/author_list/')


def edit_author(request):
    id = request.GET.get('id')
    author_obj = Author.objects.get(id=id)

    if request.method == 'POST':
        books_list = request.POST.getlist('books')
        author = request.POST.get('author')

        author_obj.author = author
        author_obj.save()
        author_obj.books.set(books_list)
        return redirect('/author_list/')

    all_books = Book.objects.all()
    author_obj = Author.objects.get(id=id)
    return render(request, 'edit_author.html', {'author_obj': author_obj, 'all_books': all_books})


def upload_book(request):
    book_file_obj = request.FILES.get('book_file')
    # print(book_file_obj.name)

    if request.method == 'POST':
        if os.path.exists(BASE_DIR + '\\' + book_file_obj.name):
            print('文件名重复')
            return redirect('/upload_book/')

        with open(book_file_obj.name, 'wb') as f:
            for chunks in book_file_obj.chunks(1024):
                f.write(chunks)
        f.close()
    return render(request, 'upload_book.html')


def edit_bookfile(request):
    id = request.GET.get('id')
    book_obj = Book.objects.get(id=id)
    if request.method == 'POST':
        book_file = request.FILES.get('book_file')
        with open(BASE_DIR + '\\static\\uploads\\' + book_file.name, 'wb') as f:
            for chunks in book_file.chunks(1024):
                f.write(chunks)
        f.close()
        new_bookfile = BookFile.objects.create(filename=book_file.name)

        tmplst = []
        for i in book_obj.filename.all():
            tmplst.append(i.id)
        tmplst.append(new_bookfile)

        book_obj.filename.add(*tmplst)

    return render(request, 'edit_bookfile.html', {'book_obj': book_obj})


def delete_bookfile(request):
    id = request.GET.get('id')
    BookFile.objects.get(id=id).delete()
    return redirect('/edit_bookfile/?id=' + id)
