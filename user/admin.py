from django.contrib import admin
from .models import Account, Follow
from django.utils.translation import gettext as _


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'from_user'    
    

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_active', 'email', 'created_at', 'deleted')
    list_filter = ('is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email', 'deleted')
    actions = ['undelete_accounts']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'bio', 'image', 'email', 'phone_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_verify', 'is_staff', 'is_admin'),
            'classes': ('collapse',)
        }),
        (_("Date Information"), {
            'fields': ('date_of_birth',),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [FollowInline]


    def undelete_accounts(self, request, queryset):
        for account in queryset:
            account.undelete()
        self.message_user(request, 'Selected accounts have been undeleted.')
    undelete_accounts.short_description = 'Undelete selected accounts'
    

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')
    search_fields = ('from_user', 'to_user')    