from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Avatar, Follow
from django.utils.translation import gettext_lazy as _

admin.site.register(Avatar)
admin.site.register(Follow)

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'email', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fullname', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'fullname', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'fullname')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
