from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')


# --> 出版社
class Press(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='出版社名称')

    def __str__(self):
        return self.name


# --> 书
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, verbose_name='书名')
    press = models.ForeignKey(to='Press', on_delete=models.CASCADE)
    filename = models.ManyToManyField(to="BookFile")


# --> 书  文件
class BookFile(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100)
    # book = models.ForeignKey(to='Book', on_delete=models.CASCADE, null=True, blank=True)


# -->作者
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=20)
    books = models.ManyToManyField(to='Book')
