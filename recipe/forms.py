from django import forms

from .models import Recipe, Comment, Like


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "description", "instructions", "time_to_cook", "image", "category")


class RecipeAddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        
class RecipeAddLikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []