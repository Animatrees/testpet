from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'show_photo', 'photo', 'email', 'first_name', 'last_name', 'date_birth', 'is_staff',
                    'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('photo', 'date_birth')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('photo', 'date_birth')}),
    )

    @admin.display(description='Фото')
    def show_photo(self, user: User):
        if user.photo:
            return mark_safe(f'<img src="{user.photo.url}" alt="Фото для {user.username}" width=70')


admin.site.register(User, CustomUserAdmin)
