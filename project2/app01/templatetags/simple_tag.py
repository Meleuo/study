from django import template
from project2.settings import STATIC_URL

register = template.Library()

@register.simple_tag(name='divtag')
def divtag(*args, **kwargs):
    return '%s_%s' % ({'args': args, 'kwargs': kwargs}, STATIC_URL)
