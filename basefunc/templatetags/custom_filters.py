from django import template
from django.template.defaultfilters import slugify

register = template.Library()


@register.filter(name='db2')
def divide_by_2(value):
    try:
        return int(value) // 2
    except ValueError:
        return 0


@register.filter
def add_string(value, arg):
    return value + arg


def custom_function(value):
    # Используем фильтр slugify
    return slugify(value)
