from django import template

register = template.Library()


@register.filter
def tiene_cargo(user, cargo):
    """
    Verifica si el usuario tiene un cargo específico.

    Uso en template:
        {% if request.user|tiene_cargo:"administrador" %}
    """
    if not hasattr(user, 'cargo'):
        return False
    return user.cargo == cargo


@register.filter
def cargo_en(user, cargos):
    """
    Verifica si el usuario tiene uno de varios cargos separados por coma.

    Uso en template:
        {% if request.user|cargo_en:"administrador,cocinero" %}
    """
    if not hasattr(user, 'cargo'):
        return False
    lista = [c.strip() for c in cargos.split(',')]
    return user.cargo in lista


@register.simple_tag(takes_context=True)
def es_admin(context):
    """
    Tag simple para verificar si es administrador.

    Uso en template:
        {% es_admin as admin %}
        {% if admin %} ... {% endif %}
    """
    request = context.get('request')
    if request and hasattr(request.user, 'cargo'):
        return request.user.cargo == 'administrador'
    return False