from typing import Any
from django.db import models
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.db.models import Count

from .models import Recipe

class RecipeListView(View):
    template_name = "recipes/recipe_list.html"
    def get(self, request, *args, **kwargs):
        qs = Recipe.objects.annotate(like_count=Count("likes")).prefetch_related("likes").all()
        context = {"recipes": qs}
        return render(request, self.template_name, context)
    
    
class RecipeDetailView(DetailView):
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"
    queryset = Recipe.objects.annotate(like_count=Count("likes")).prefetch_related("likes", "comments")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.queryset[0].comments.all()
        return context
            