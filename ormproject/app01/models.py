from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    birth = models.DateTimeField(auto_now_add=True)


class Press(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Books(models.Model):
    press = models.ForeignKey(Press, on_delete=models.CASCADE, related_name='books')
    author = models.ManyToManyField(Author, related_name='books')
    name = models.CharField(max_length=10)
    price = models.IntegerField()
    sales = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name