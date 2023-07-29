from django.urls import path, include

from .views import (
    RecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    RecipeCategoryList,
    HomeView
    )

app_name = "recipe"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list/', RecipeListView.as_view(), name='list'),
    path('<int:pk>/detail/', RecipeDetailView.as_view(), name='detail'),
    path("create/", RecipeCreateView.as_view(), name='create'),
    path("category/<slug:cat>/", RecipeCategoryList.as_view(), name='category'),
    
    path("<int:pk>/update/", RecipeUpdateView.as_view(), name='update'),
    path("<int:pk>/delete/", RecipeDeleteView.as_view(), name='delete'),
]
