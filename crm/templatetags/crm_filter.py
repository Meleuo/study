from django import template
from django.shortcuts import reverse

register = template.Library()


@register.filter(name='get_url_active')
def get_url_active(value, args):
    try:
        # if value == 'consult_record_list':
        #     if 'consult_record/list/' in args:
        #         return 'active'
        if reverse(value) == args:
            return 'active'
        return ''
    except Exception as e:
        return ''
