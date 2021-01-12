from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
import random


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        v_code = request.POST.get('v_code', '').lower()
        if v_code != request.session.get('v_code'):  # --> 用户提交登录时先校验验证码, 从session中读取验证码的内容, 在比较用户提交过来的验证码内容
            return render(request, 'login.html', {'error_msg': '验证码出错'})

        if username != 'admin' or password != '1':
            return render(request, 'login.html', {'error_msg': '认证出错'})
        return redirect('http://www.baidu.com')


def code_img():
    def color() -> (int, int, int):
        # 生成一个rgb颜色组
        color1 = random.randint(0, 255)
        color2 = random.randint(0, 255)
        color3 = random.randint(0, 255)
        return color1, color2, color3

    img_obj = Image.new('RGB', (170, 50), color())  # --> 创建一张纯色图片
    img_obj_draw = ImageDraw.Draw(img_obj)  # --> 这纯色图片上创建画布

    img_font = ImageFont.truetype('static/font/kumo.ttf', 40)  # --> 设置一个ImageFont对象, 定义 字体, 以及字体大小

    _code = ''  # --> 空字符串用于保留验证码
    for i in range(4):
        # --> 在画布上插入4个随机字符组成验证码
        str1 = chr(random.randint(75, 90))
        str2 = chr(random.randint(97, 122))
        str3 = str(random.randint(0, 9))
        str4 = random.choice([str1, str2, str3])

        img_obj_draw.text((40 * i, 3), str4, fill=color(), font=img_font)
        _code += str4

    width = 170  # 图片宽度（防止越界）
    height = 50
    for i in range(5):
        # 给图片加干扰线
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        img_obj_draw.line((x1, y1, x2, y2), fill=color())

    from io import BytesIO  # --> 从IO模块中导入BytesIO方法
    f = BytesIO()  # -->    在内存中开辟一块存放bytes数据的区域
    img_obj.save(f, 'PNG')  # --> 将验证码图片保存在内存当做, 这样就不用落盘了
    return f.getvalue(), _code  # --> 然后 从内存中读取图片的二进制内容, 以及验证码字符


class V_Code(View):
    def get(self, request):
        code_png, code_text = code_img()
        request.session['v_code'] = code_text.lower()  # -->将验证码转换为小写, 放在本地的session中用于校验
        print(code_text)
        return HttpResponse(code_png, content_type='image/png')  # --> 返回图片
