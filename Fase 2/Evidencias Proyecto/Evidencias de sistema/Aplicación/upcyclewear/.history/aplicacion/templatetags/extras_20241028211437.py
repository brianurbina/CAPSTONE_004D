from django import template

register = template.Library()

@register.filter
def range_filter(end):
    """Genera un rango de números desde 1 hasta end."""
    return range(1, end + 1)
