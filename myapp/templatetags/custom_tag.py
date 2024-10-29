from django import template
import re

register = template.Library()

@register.simple_tag
def add_class(x, y, z="highlight"):   
    highlighted = re.sub(re.escape(y), f'<span class="{z}">{y}</span>', x)
    return highlighted