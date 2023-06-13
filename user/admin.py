from django.contrib import admin
from .models import Account, Follow


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'followed_user'


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
    inlines = [FollowInline]

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('following_user', 'followed_user')
    search_fields = ('following_user', 'followed_user')