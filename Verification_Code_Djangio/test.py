from PIL import Image
import random


# --> 生成随机验证码
def random_code():
    lst = []
    for i in range(4):
        str1 = chr(random.randint(65, 90))
        str2 = chr(random.randint(95, 122))
        str3 = str(random.randint(0, 9))
        lst.append(random.choice([str1, str2, str3]))
    return ''.join(lst)


# --> 画一张纯色图
def _drawing() -> None:
    from PIL import Image
    # Image.new('图片模式,RGb即可', (长, 高), 颜色码)
    img_obj = Image.new('RGB', (200, 50), (255, 255, 255))
    with open('./testimg1.png', 'wb') as f:
        img_obj.save(f, format='PNG')  # save保存图片, 第一个就是文件对象, 第二个是格式


# --> 将文本写到一张图片上
def _str_reach_img() -> None:
    from PIL import Image, ImageDraw
    # Image.new('图片模式,RGb即可', (长, 高), 颜色码)
    img_obj = Image.new('RGB', (200, 50), (255, 255, 255))

    img_obj_draw = ImageDraw.Draw(img_obj)  # -->将生成的纯色图片传递给画板函数

    #
    # img_obj_draw.text((x轴, y轴), '内容', fill=颜色, font=字体)
    img_obj_draw.text((20, 0), 'content', fill=(38, 50, 56))

    with open('./testimg2.png', 'wb') as f:
        img_obj.save(f, format='PNG')  # save保存图片, 第一个就是文件对象, 第二个是格式


# _str_reach_img()

# --> 在图片上画线 and 点
def _point_line_img():
    from PIL import Image, ImageDraw
    img_obj = Image.new('RGB', (200, 50), (255, 255, 255))
    img_obj_draw = ImageDraw.Draw(img_obj)
    img_obj_draw.arc((5, 5, 10, 10), 1, 1000, fill=(88, 157, 246))

    with open('./testimg3.png', 'wb') as f:
        img_obj.save(f, format='PNG')



ret = 'dwqdqwd'.lower()
print(ret)