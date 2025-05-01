from django import template

from core.acyclic import Category

register = template.Library()

@register.simple_tag()
def dag_graph_data(start_node=None):
    return Category.objects.dag_cytograph_data(start_node)
