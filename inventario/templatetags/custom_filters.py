from django import template

register = template.Library()

@register.filter(name='absolute')
def absolute(value):
    """Devuelve el valor absoluto del número."""
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return value
