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
    active_item = None
    active_parents = []

    for item in all_items:
        if item.get_absolute_url() == request.path:
            active_item = item
            while active_item.parent is not None:
                active_parents.append(active_item.parent)
                active_item = active_item.parent

    for item in all_items:
        if item.parent is None:
            menu_tree[item] = []

        item.active = item == active_item or item in active_parents

        if (
            item == active_item
            or item in active_parents
            or (item.parent == active_item and active_item is not None)
        ):
            if item.parent:
                menu_tree[item.parent].append(item)

    return {"menu_items": menu_tree}
