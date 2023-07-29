from django.urls import path

from .views import (
    RecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    RecipeAddComment,
    RecipeAddLike,
    RecipeAddToFavorite,
    )

app_name = "recipe"

urlpatterns = [
    path('', RecipeListView.as_view(), name='list'),
    path('<int:pk>/detail/', RecipeDetailView.as_view(), name='detail'),
    path("create/", RecipeCreateView.as_view(), name='create'),
    path("<int:pk>/update/", RecipeUpdateView.as_view(), name='update'),
    path("<int:pk>/delete/", RecipeDeleteView.as_view(), name='delete'),
    path("<int:pk>/comment/", RecipeAddComment.as_view(), name='comment'),
    path("<int:pk>/like/", RecipeAddLike.as_view(), name='like'),
    path("<int:pk>/fav/", RecipeAddToFavorite.as_view(), name='favorite'),
]
