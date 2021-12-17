from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Profile


class UserAdmin(BaseUserAdmin):
    readonly_fields = ['created_at', 'updated_at']
    list_display = ('id', 'email', 'mobile', 'first_name', 'last_name', 'is_superuser', 'is_active')
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        ('Security information', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
        ('Important date', {'fields': ('created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2'),
        }),
    )
    search_fields = ('first_name', 'last_name')
    ordering = ('-id',)
    filter_horizontal = ()


admin.site.register(get_user_model(), UserAdmin)
admin.site.unregister(Group)

admin.site.register(Profile)
