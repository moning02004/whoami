import re

import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def replace_introduction(instance):
    year = str(int(sum([x.career_year for x in instance.resumecareer_set.all()])))
    introduction = instance.introduction.replace("{{ year }}", year)
    return introduction


@register.filter
def to_markdown(value):
    value = value.replace('\r\n', '\n')
    value = re.sub(r'\n{1}', '\n\n', value)
    value = re.sub(r'\n{3,}', '\n\n<br>\n\n', value)
    return mark_safe(markdown.markdown(value))


@register.filter
def split(value, sep="\n"):
    return value.replace("\r", "").split(sep)