from django import template

register = template.Library()

@register.filter
def enumerate_list(value, start=0):
    return [(index + start, item) for index, item in enumerate(value)]
