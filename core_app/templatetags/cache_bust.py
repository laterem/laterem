import os
import uuid
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(name='cache_bust')
def cache_bust():

    if settings.DEBUG:
        version = uuid.uuid1()
    else:
        version = os.environ.get('PROJECT_VERSION')
        if version is None:
            version = '1'
            os.environ['PROJECT_VERSION'] = version

    return f'__v__={version}'
