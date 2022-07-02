from django import template

register = template.Library()


@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.input_type
