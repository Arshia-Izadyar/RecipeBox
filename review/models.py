from django.db import models
from recipe.models import Recipe
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, verbose_name=_("User"))
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Recipe"))
    content = models.TextField(verbose_name=_("Content"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created date"))
    
    def __str__(self):
        return f"{self.user} - {self.created_date}"
    


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE, verbose_name=_("User"))
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="likes", verbose_name=_("Recipe"))
    class Meta:
        unique_together = ('user', 'recipe')
        

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE, verbose_name=_("User"))
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorites", verbose_name=_("Recipe"))
    
    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        unique_together = ('user', 'recipe')
        unique_together = ('user', 'recipe')
        
    def __str__(self):
        return f"{self.user} - {self.recipe}"
    