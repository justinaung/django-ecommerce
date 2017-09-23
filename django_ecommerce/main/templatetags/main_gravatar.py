from urllib.parse import urlencode
import hashlib

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def gravatar_img(email: str, size="140"):
    print('User email: ', email)
    url = gravatar_url(email, size)
    return mark_safe(f'<img class="img-circle" src="{url}" '
                     f'height="{size}" width="{size}" alt="user.avatar" />')


@register.simple_tag
def gravatar_url(email: str, size="140"):
    deafult = ('http://upload.wikimedia.org/wikipedia/en/9/9b/'
               'Yoda_Empire_Strikes_Back.png')

    if not(isinstance(email, str)):
        return deafult

    query_params = urlencode([('s', str(size)),
                              ('d', deafult if not email else email)])

    return ('http://www.gravatar.com/avatar/'
            + hashlib.md5(email.lower().encode('utf-8')).hexdigest()
            + '?'
            + query_params)
