from django import template

register = template.Library()

@register.filter
def range_filter(start, end):
    """Genera un rango de números desde start hasta end."""
    return range(start, end + 1)
