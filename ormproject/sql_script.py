import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ormproject.settings")
    import django

    django.setup()

    from app01.models import Author, Press, Books
    from django.db.models import Avg, Sum, Max, Min, Count
    from django.db.models import F, Q

    # ret = Press.objects.values('books__name').filter(books__stock__lt=F('books__sales'))

    # ret = Books.objects.filter(Q(sales__gt=500) | Q(stock__lt=100)).values()
    # [print(i) for i in ret]

    ret = Books.objects.filter(Q(sales__gt=500) | Q(stock__lt=100)).values()
    [print(i) for i in ret]



    # ret = Author.objects.all().aggregate(min_age=Min('age'), max_age=Max('age'), avg_age=Avg('age'))

    # ret = Books.objects.aggregate(price_max=Max('price'), price_min = Min('price'))
    # print(ret)

    # ret = Books.objects.annotate(Sum('price'))

    # ret = Press.objects.values('name').annotate(books_num=Count('books'))
    # print(ret)

    # ret = Books.objects.annotate(author_num=Count('author')).filter(author_num__gt=1)
    # print(ret)
    # print(Books.objects.get(name='建国回忆录').author.values('name'))
    # ret = Press.objects.values('name').annotate(price_min=Min('books__price'))
    # [print(i) for i in ret]
    # ret = Author.objects.values('name').annotate(book_price=Sum('books__price')).order_by('book_price')
    # [print(i) for i in ret]

    # ret = Author.objects.last()
    # print(ret.books.all())
    # ret = Books.objects.values('name').annotate(author_num=Count('author')).order_by('-author_num')
    # [print(i) for i in ret]
    # ret = Author.objects.filter(id__gt=2).values('id','name')
    #
    # ret = Author.objects.get(id=5)
    # print(ret)
    # # print(ret.books_set.add(*Books.objects.filter(name__contains='建国')))
    # print(ret.books_set.remove(*Books.objects.filter(name__contains='建国')))
    # print(ret.books_set.all())

    # ret = Books.objects.get(name='建国回忆录')
    # # ret.author.set(Author.objects.all())
    #
    # print(ret.author.all())
    # # ret.author.set(Author.objects.all())
    # print(ret.author.remove(5))
    # print(ret.author.all())

    # print(ret.books.all())
    # ret.books_set.set(Books.objects.filter(id=2))
    # ret.books_set.clear()
    # ret = Books.objects.filter(press_id=Press.objects.filter(name='建国出版社')[0].id)
    # print(ret)
    #
    # ret = Books.objects.filter(press__name__contains='建国出版社')
    # print(ret)
    #
    # ret = Books.objects.first()
    # print(ret.press.name)

    # ## 正向查询
    # ret = Books.objects.all().values('name', 'press__name')
    #
    # ret = Press.objects.filter()
    #
    # ret = Books.objects.filter(id=Press.objects.get(name='建国出版社').id)
    # print(ret)
    # ret = Books.objects.filter(press__name='建国出版社')
    # print(ret)
    #
    #
    # ## 反向查询
    # ret = Press.objects.get(name='振华出版社')
    # print(ret.books_set.values('name'))
