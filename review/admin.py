from django.contrib import admin

from .models import Comment, Like, Favorite

   
    
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")    
    
@admin.register(Comment)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user", "content")
    
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")