# def fun2(fun):
#     def wrapper(*args, **kwargs):
#         print(args)
#         print(kwargs)
#         print('汤姆过来了')
#         return fun(*args, **kwargs)
#
#     return wrapper
#
#
# @fun2
# def fun1(helper):
#     print('Jerry 逃跑了')
#     if helper:
#         print('杰瑞大表哥来了')
#     return 'Yes'
#
# print(fun1(helper=True))


class A1(object):
    def __init__(self):
        pass

    @staticmethod
    def b1():
        print('b1')

    @classmethod
    def b2(cls):
        print('b1', cls)
        return  cls

a1 = A1()
a1.b1()
b2 = a1.b2()
b2().b1()

