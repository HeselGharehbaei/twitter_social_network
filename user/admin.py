from django.contrib import admin
from .models import Account, Follow
from django.utils.translation import gettext as _


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'from_user'    
    

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_active', 'email', 'created_at', 'deleted', 'followers_count')
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


    def followers_count(self, obj):
        following_count, following, followers_count, followers = obj.get_followers_and_following_count()
        return followers_count


    def undelete_accounts(self, request, queryset):
        for account in queryset:
            account.is_active = True
            account.save()
            if account.is_active and account.post_set.filter(is_archived=True).exists():
                for post in account.post_set.filter(is_archived=True):
                    post.is_archived = False
                    post.save()

    undelete_accounts.short_description = "Undelete selected accounts and unarchive their posts"
    

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')
    search_fields = ('from_user', 'to_user')    