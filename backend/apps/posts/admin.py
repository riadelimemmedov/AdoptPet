from django.contrib import admin

from .models import Category, Comment, Post

# Register your models here.


# !CategoryAdmin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "created", "modified"]
    list_display_links = ["id", "name"]


# !PostAdmin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug", "created", "modified"]
    list_display_links = ["id", "title"]


# !CommentAdmin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "modified"]
    list_display_links = ["id"]
