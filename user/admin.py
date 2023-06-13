from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'first_name', 'last_name', 'acctive', 'image')
    list_filter = ('acctive',)
    search_fields = ('user_name', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('user_name', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'image')}),
        ('Permissions', {'fields': ('acctive',)}),
    )
