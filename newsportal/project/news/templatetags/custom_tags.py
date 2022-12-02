from django import template
from datetime import datetime


register = template.Library()


@register.simple_tag(name='current_date')
def current_date(date_format='%b %d %Y'):
    return datetime.utcnow().strftime(date_format)


@register.simple_tag(name='url_replace', takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
