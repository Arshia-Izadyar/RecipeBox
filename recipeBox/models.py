from django.db import models
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

User = get_user_model()

    
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    parent = models.ForeignKey('self', related_name="children", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Recipe(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Created time"))
    modified_time = models.DateTimeField(verbose_name=_("Modified time"))
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.CharField(blank=True, null=True, verbose_name=_("Description"))
    instructions = models.TextField(verbose_name=_("Instructions"))
    time_to_cook = models.DurationField(verbose_name=_("time to cook"))
    image = models.ImageField(upload_to="images/", verbose_name=_("Image"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe", verbose_name=_("User"))
    # like = models.PositiveBigIntegerField(default=0, )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="categories", verbose_name=_("Category"))
    
    def __str__(self):
        return f"{self.title} - {self.created_time}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, verbose_name=_("User"))
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Recipe"))
    content = models.TextField(verbose_name=_("Content"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created date"))
    lol = models.TextField()
    
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
        
    def __str__(self):
        return f"{self.user} - {self.recipe}"
    