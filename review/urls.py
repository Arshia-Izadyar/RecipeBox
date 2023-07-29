from django.urls import path

from .views import (
    RecipeAddComment,
    RecipeAddLike,
    RecipeAddToFavorite,
    )

app_name = "review"

urlpatterns = [
    path("<int:pk>/comment/", RecipeAddComment.as_view(), name='comment'),
    path("<int:pk>/like/", RecipeAddLike.as_view(), name='like'),
    path("<int:pk>/fav/", RecipeAddToFavorite.as_view(), name='favorite'),
]
