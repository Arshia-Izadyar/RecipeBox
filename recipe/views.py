from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView, DeleteView
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Recipe, Comment
from .forms import RecipeForm, RecipeAddCommentForm, RecipeAddLikeForm, RecipeFavoritesForm

class RecipeListView(View):
    template_name = "recipes/recipe_list.html"
    def get(self, request, *args, **kwargs):
        qs = Recipe.objects.annotate(like_count=Count("likes")).prefetch_related("likes").all()
        context = {"recipes": qs}
        return render(request, self.template_name, context)
    
    
class RecipeDetailView(DetailView):
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Recipe.objects.annotate(like_count=Count("likes")).prefetch_related("likes", "comments").filter(pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = context['recipe']
        context["comments"] = recipe.comments.all()
        context["comment_form"] = RecipeAddCommentForm()
        context["like_form"] = RecipeAddLikeForm()
        return context
            
"""           
class RecipeCreateView(LoginRequiredMixin, FormView):
    form_class = RecipeForm
    
    template_name = "recipes/recipe_create.html"
    success_url = "/"
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)
"""       

class RecipeCreateView(View):
    template_name = "recipes/recipe_create.html"
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = RecipeForm
        context = {"form": form}
        return render(request, self.template_name,context)
    def post(self, request, *args, **kwargs):
        form = RecipeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect("/")
        raise Http404
    
class RecipeUpdateView(UpdateView):
    template_name = "recipes/recipe_update.html"
    form_class = RecipeForm
    context_object_name = "recipe"
    success_url = "/"
    
    def get_queryset(self):
        return Recipe.objects.filter(pk=self.kwargs['pk'])
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
    
    
class RecipeDeleteView(DeleteView):
    template_name = "recipes/recipe_confirm_delete.html"
    model = Recipe
    success_url = "/"
    
    def dispatch(self, request, *args, **kwargs):
        self.obj = self.get_object()
        if request.user == self.obj.user: # if user in owner
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
        
    def get_queryset(self):
        return Recipe.objects.filter(pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.obj.delete()
            return HttpResponseRedirect(self.success_url)


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