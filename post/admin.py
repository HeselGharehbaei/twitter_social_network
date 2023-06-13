from django.contrib import admin
from .models import Post, Tag, Comment, Image


class ImageInline(admin.TabularInline):
    model = Image


class CommentInline(admin.StackedInline):
    model = Comment


class TagInline(admin.TabularInline):
    model = Tag
    fk_name = 'post'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')  
    list_filter = ('user', 'acctive')
    search_fields = ('title', 'tag')
    inlines = [ImageInline, CommentInline, TagInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image',)   


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text',) 
    list_display = ('title', 'post', 'created_at')
    list_filter = ('post',)
     