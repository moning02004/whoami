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
    return mark_safe(markdown.markdown(value))
