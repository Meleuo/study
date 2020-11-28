from django import template

register = template.Library()


@register.inclusion_tag(name='div_inclusion', filename='index2.html')
def div_inclusion(*args, **kwargs):
    print(args)
    return {'number': range(1, args[0] + 1)}