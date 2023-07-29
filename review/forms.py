from django import forms

from .models import Comment, Like, Favorite

class RecipeAddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        
class RecipeAddLikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []
        
class RecipeFavoritesForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = []