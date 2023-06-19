from django.contrib import admin
from .models import Account, Follow
from django.utils.translation import gettext as _


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'from_user'    
    

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'email')
    list_filter = ('is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'image', 'email')}),
        ('Permissions', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
        (_("Date Information"), {
            'fields': ('date_of_birth',),
            'classes': ('collapse',)
        }),
    )

    inlines = [FollowInline]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')
    search_fields = ('from_user', 'to_user')    