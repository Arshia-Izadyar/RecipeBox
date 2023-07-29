from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Recipe
from .forms import RecipeAddCommentForm, RecipeAddLikeForm, RecipeFavoritesForm


class RecipeAddComment(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        pk =self.kwargs['pk']
        form = RecipeAddCommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.recipe = Recipe.objects.get(pk=pk)
            obj.save()
            return HttpResponseRedirect(reverse_lazy("recipe:detail", kwargs={"pk":pk}))
        return HttpResponseRedirect('/')


class RecipeAddLike(View):
    # or i can add like to existing model 
    # obj.like += 1
    # obj.save()    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        form = RecipeAddLikeForm(request.POST) 
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.recipe = Recipe.objects.get(pk=pk)
            obj.save()
            return HttpResponseRedirect(reverse_lazy("recipe:detail", kwargs={"pk":pk}))
        return HttpResponseRedirect('/')
    
class RecipeAddToFavorite(LoginRequiredMixin, DetailView):
    model = Recipe
    
    def get_queryset(self):
        return Recipe.objects.filter(pk=self.kwargs.get('pk'))
    
    def post(self, request, *args, **kwargs):
        form = RecipeFavoritesForm(request.POST)
        obj = self.get_object()
        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = request.user
            favorite.recipe = obj
            favorite.save()
            return HttpResponseRedirect(reverse_lazy("recipe:detail", kwargs={"pk":self.kwargs.get('pk')}))
        return HttpResponseRedirect('/')
    
class RecipeRemoveFavorite(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            obj = get_object_or_404(Recipe, pk=pk)  
            obj.delete()
            
        except Recipe.DoesNotExist:
            return HttpResponseRedirect("/")
        return HttpResponseRedirect(reverse_lazy('recipe:home'))