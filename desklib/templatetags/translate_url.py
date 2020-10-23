
from django import template
from django.urls import reverse, resolve
from django.utils import translation
from typing import Optional, Any, Dict

from django import urls


register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context: Dict[str, Any], language: Optional[str]) -> str:
    url = context['request'].build_absolute_uri()
    return urls.translate_url(url, language)


@register.filter
def mask_email_domain(email):
    lo = email.find('@')
    if lo > 0:
        return email[0:2] + "******" + email[lo - 2:]
    else:
        return email
