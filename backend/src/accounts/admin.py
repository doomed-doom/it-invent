from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "username",
        "email",
        "full_name",
        "Организация",
        "Подразделение",
        "Телефон",
        "Роль",
        "date_joined_display",
    )

    def full_name(self, obj):
        return f"{obj.Фамилия} {obj.Имя} {obj.Отчество}"

    full_name.short_description = "ФИО"

    def date_joined_display(self, obj):
        return obj.date_joined if obj.date_joined else "-"

    date_joined_display.short_description = "Дата регистрации"

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Личная информация",
            {
                "fields": (
                    "Имя",
                    "Фамилия",
                    "Отчество",
                    "email",
                    "Телефон",
                    "Организация",
                    "Подразделение",
                )
            },
        ),
        (
            "Права доступа",
            {"fields": ("is_active", "is_superuser", "groups", "user_permissions")},
        ),
        ("Роль", {"fields": ("Роль",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "Роль",
                    "email",
                    "Имя",
                    "Фамилия",
                    "Отчество",
                    "Телефон",
                    "Организация",
                    "Подразделение",
                ),
            },
        ),
    )
