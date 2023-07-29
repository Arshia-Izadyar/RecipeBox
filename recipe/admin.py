from django.contrib import admin

from .models import Category, Comment, Like, Favorite, Recipe
from .permissions import IsAuthorOrReadOnlyPermission

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "parent")
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_time")
    search_fields = ("title", "user")
    order_by = ("-created_time")
    
    def get_model_perms(self, request):
        return {
            'change': IsAuthorOrReadOnlyPermission('change', self, Recipe),
            'delete': IsAuthorOrReadOnlyPermission('delete', self, Recipe),
        }
    
    
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")    
    
@admin.register(Comment)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user", "content")