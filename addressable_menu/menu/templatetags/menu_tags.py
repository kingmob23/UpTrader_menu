from django import template

from ..models import MenuItem

register = template.Library()


@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    request = context["request"]
    all_items = (
        MenuItem.objects.filter(menu_name=menu_name)
        .select_related("parent")
        .order_by("parent__id")
    )

    menu_tree = {}
    for item in all_items:
        if item.parent is None:
            menu_tree[item] = []

        if item.get_absolute_url() == request.path:
            item.active = True
        else:
            item.active = False

        if item.parent:
            menu_tree[item.parent].append(item)

    return {"menu_items": menu_tree}
