from django.db import models


class User(models.Model):
    username = models.CharField(verbose_name='管理员用户名', max_length=10)
    password = models.CharField(verbose_name='管理员密码', max_length=20)

    def __str__(self):
        return self.username


class Author(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=10)

    def __str__(self):
        return 'Author: %s' % self.username


class Press(models.Model):
    press_name = models.CharField(verbose_name='出版社名称', max_length=10)

    def __str__(self):
        return 'press_name: %s' % self.press_name


class BookFile(models.Model):
    file_title = models.CharField(verbose_name='文件标题', max_length=20)
    file_path = models.CharField(verbose_name='文件路径', max_length=200)

    def __str__(self):
        return 'file_title: %s' % self.file_title


class Book(models.Model):
    book_author = models.ManyToManyField(Author, verbose_name='作者')
    book_press = models.ManyToManyField(Press)
    book_file = models.ManyToManyField(BookFile)
    book_name = models.CharField(verbose_name='书名', max_length=10)

    def __str__(self):
        return 'Book: %s' % self.book_name





