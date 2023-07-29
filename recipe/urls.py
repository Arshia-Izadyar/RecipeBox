from django.urls import path

from .views import RecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView

app_name = "recipe"

urlpatterns = [
    path('', RecipeListView.as_view(), name='list'),
    path('<int:pk>/detail/', RecipeDetailView.as_view(), name='detail'),
    path("create/", RecipeCreateView.as_view(), name='create'),
    path("<int:pk>/update/", RecipeUpdateView.as_view(), name='update'),
    path("<int:pk>/delete/", RecipeDeleteView.as_view(), name='delete'),
]
