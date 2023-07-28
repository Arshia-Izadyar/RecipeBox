from django.contrib import admin

from .models import Category, Comment, Like, Favorite, Recipe

@admin.register(Category)
class CategoryAdmin(admin.TabularInline):
    list_display = ("name", "parent")
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (CategoryAdmin,)
    list_display = ("title", "user", "created_time")
    search_fields = ("title", "user")
    order_by = ["-created_time"]