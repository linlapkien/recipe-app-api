"""
Django admin customizations
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

""" import all the custome models that we want to register in django admin"""
from core import models


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users. """
    ordering = ['id']
    list_display = ['email', 'name']

    """ Fieldsets is a tuple. """
    """ None is the title of the section. """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']

    """ Add fieldsets for creating user. """
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )

admin.site.register(models.User, UserAdmin)
