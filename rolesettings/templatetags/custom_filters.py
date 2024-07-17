# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Splits the value by the specified key.
    """
    return value.split(key)
