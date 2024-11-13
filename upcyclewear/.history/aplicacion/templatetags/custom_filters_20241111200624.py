from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={'class': css_class})
    # Si no es un campo de formulario, simplemente devuelve el valor original.
    return field



@register.filter(name='calculate_percentage')
def calculate_percentage(value, total=15):
    if value is None:
        return 0
    return (value / total) * 100
