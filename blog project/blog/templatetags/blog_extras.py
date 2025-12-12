from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter
def render_markdown(value):
    """Render Markdown content to HTML."""
    if not value:
        return ''
    html = markdown.markdown(value, extensions=['fenced_code', 'tables'])
    return mark_safe(html)


@register.filter(name='add_attrs')
def add_attrs(field, attrs):
    """Apply a space-delimited list of attribute assignments to a form field widget."""
    if not hasattr(field, 'field'):
        return field
    attr_pairs = [attr.strip() for attr in attrs.split(',') if attr.strip()]
    new_attrs = dict(field.field.widget.attrs)
    for pair in attr_pairs:
        key, _, value = pair.partition('=')
        if key and value:
            if key == 'class' and new_attrs.get('class'):
                new_attrs['class'] = f"{new_attrs['class']} {value}".strip()
            else:
                new_attrs[key] = value
    return field.as_widget(attrs=new_attrs)
