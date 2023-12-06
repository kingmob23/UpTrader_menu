from django.contrib import admin

from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "menu_name", "parent")
    list_filter = ("menu_name",)
    search_fields = ("title", "url", "named_url")
