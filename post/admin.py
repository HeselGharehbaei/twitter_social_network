from django.contrib import admin
from django.utils.translation import gettext as _
from .models import Post, Tag, Image, Comment, Like


class ImageInline(admin.TabularInline):
    model = Image
    classes = ['collapse']

class CommentInline(admin.TabularInline):
    model = Comment
    classes = ['collapse']


class LikInline(admin.TabularInline):
    model = Like   
    classes = ['collapse']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInline, CommentInline, LikInline]
    list_display = ('title', 'user', 'created_at', 'is_archived')
    list_filter = ('is_archived', 'tags')
    search_fields = ('title', 'text')
    filter_horizontal = ('tags',)
    fieldsets = (
        (_("Post Information"), {
            'fields': ('user', 'title', 'text', 'tags', 'is_archived')
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'like')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'parent')
    list_filter = ('post',)
    search_fields = ('title', 'text')
    fieldsets = (
        (_("Comment Information"), {
            'fields': ('text', 'parent', 'user', 'post')
        }),
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'alt', 'Post')