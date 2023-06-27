from django.contrib import admin
from .models import Account, Follow
from django.utils.translation import gettext as _


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'from_user' 


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'email', 'date_joined', 'followers_count', 'following_count')
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
    inlines = [FollowInline]


    def followers_count(self, obj):
        following_count, following, followers_count, followers = obj.get_followers_and_following()
        return followers_count  


    def following_count(self, obj):
        following_count, following, followers_count, followers = obj.get_followers_and_following()
        return following_count   
 

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')
    search_fields = ('from_user', 'to_user')  