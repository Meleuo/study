from django import template
from django.shortcuts import reverse

register = template.Library()


@register.filter(name='get_url')
def get_url(value):
    if not reverse(value):
        return ''
    return reverse(value)
