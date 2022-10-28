from django import template
from os.path import join as pathjoin

register = template.Library()

@register.simple_tag(takes_context=True)
def asset(context, format_string):
    taskname = context['meta_taskname']
    path = '/taskasset' + '/' + taskname + '/' + format_string
    return path