from django.contrib import admin
from .models import Account
from django.utils.translation import gettext as _


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'email', 'date_joined')
    list_filter = ('is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'image', 'email', 'phone_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff'),
            'classes': ('collapse',)
        }),
        (_("Date Information"), {
            'fields': ('date_joined',),
            'classes': ('collapse',)
        }),
    )
 