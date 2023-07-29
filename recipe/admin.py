from django.contrib import admin

from .models import Category, Recipe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "parent")

    

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "created_time")
    search_fields = ("title", "user")
    order_by = ("-created_time")
    