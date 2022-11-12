from django import template
from datetime import datetime


register = template.Library()


@register.simple_tag(name='current_date')
def current_date(date_format='%d %M %Y'):
    return datetime.utcnow().strftime(date_format)


