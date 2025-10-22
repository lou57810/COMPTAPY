from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """Ajoute dynamiquement une classe CSS à un champ de formulaire."""
    return field.as_widget(attrs={'class': css})
