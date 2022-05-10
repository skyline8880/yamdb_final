from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
    )
    list_display_links = ("pk", "username")
    list_filter = ("role",)
    search_fields = ("username", "first_name", "last_name")
    empty_value_display = "-пусто-"
    list_editable = ("role",)
    list_per_page = 10
    list_max_show_all = 200
    readonly_fields = (
        "id",
        "username",
    )


admin.site.register(User, UserAdmin)
