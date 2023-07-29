from django.shortcuts import render
from django.views import View
from django.db.models import Count

from .models import Recipe

class RecipeListView(View):
    template_name = "recipes/recipe_list.html"
    def get(self, request, *args, **kwargs):
        qs = Recipe.objects.annotate(like_count=Count("likes")).prefetch_related("likes").all()
        context = {"recipes": qs}
        return render(request, self.template_name, context)
    
    