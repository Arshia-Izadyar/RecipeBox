from django.db import models
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

User = get_user_model()

    
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    parent = models.ForeignKey('self', related_name="children", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Recipe(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Created time"))
    modified_time = models.DateTimeField(verbose_name=_("Modified time"), auto_now=True)
    title = models.CharField(max_length=150, verbose_name=_("Title"), unique=True)
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    instructions = models.TextField(verbose_name=_("Instructions"))
    time_to_cook = models.DurationField(verbose_name=_("time to cook"))
    image = models.ImageField(upload_to="images/", verbose_name=_("Image"), null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipe", verbose_name=_("User"))
    # like = models.PositiveBigIntegerField(default=0, )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="categories", verbose_name=_("Category"))
    
    def __str__(self):
        return f"{self.title} - {self.created_time}"
    
