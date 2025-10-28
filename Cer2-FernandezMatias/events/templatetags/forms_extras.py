from django import template

register = template.Library()

@register.filter
def add_class(field, css):
    """Agrega una clase CSS a un campo de formulario."""
    return field.as_widget(attrs={"class": css})
