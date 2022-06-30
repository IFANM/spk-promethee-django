from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

# Register your models here.

from .forms import user_create_form, user_change_form
from .models import *

users = get_user_model()

class user_admin(BaseUserAdmin):
    form 	 = user_change_form
    add_form = user_create_form

    search_field		= ('email',)
    readonly_fields		= ('date_joined', 'last_login',)
    ordering			= ('email',)
    filter_horizontal	= ()
    list_display		= ('email', 'is_leader', 'is_staff',)
    list_filter			= ()

    fieldsets = (
			('Profile', {'fields': ('email', 'password',)}),
			('Permissions', {'fields': ('is_active', 'is_leader', 'is_staff',)}),
			('Important Dates', {'fields': ('date_joined', 'last_login',)}),
		)

    limited_fieldsets = (
			('Profile', {'fields': ('email', 'password',)}),
			('Important Dates', {'fields': ('date_joined', 'last_login',)}),
		)

    add_fieldsets = (
			('Profile', {
				'classes': ('wide',),
				'fields': ('email', 'password1', 'password2',),
				}),
			('Permissions', {
				'fields': ('is_active', 'is_leader', 'is_staff',),
				}),
		)


admin.site.register(users, user_admin)
admin.site.register(candidate)

# Not Use
admin.site.unregister(Group)