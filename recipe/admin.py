from django.contrib import admin

from .models import Category, Comment, Like, Favorite, Recipe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "parent")
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_time")
    search_fields = ("title", "user")
    order_by = ("-created_time")
    
    
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")