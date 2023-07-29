from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters import FilterSet
from django_filters.views import FilterView

from .models import Recipe
from .forms import RecipeForm, RecipeAddCommentForm, RecipeAddLikeForm, RecipeFavoritesForm

class HomeFilter(FilterSet):
    class Meta:
        model = Recipe
        fields = {"title": ["contains"], "category": ["exact"]}
        
"""
class RecipeListView(View):
    template_name = "recipes/recipe_list.html"
    def get(self, request, *args, **kwargs):  # commenting this because im going to use filter view
        qs = Recipe.objects.annotate(like_count=Count("likes")).prefetch_related("likes").all()
        context = {"recipes": qs}
        return render(request, self.template_name, context)
"""  

class RecipeListView(LoginRequiredMixin, FilterView):
    filterset_class = HomeFilter
    paginate_by = 10
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    model = Recipe
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(like_count=Count("likes")).prefetch_related("likes").all()
    
    
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
    
class RecipeRemoveFavorite(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            obj = get_object_or_404(Recipe, pk=pk)  
            obj.delete()
            
        except Recipe.DoesNotExist:
            return HttpResponseRedirect("/")
        return HttpResponseRedirect(reverse_lazy('recipe:home'))