from django.urls import path

from .views import(
    UserProfile,
    FollowUserView,
    UnfollowUserView,
    FollowerListView,
    FollowingListView,
    )

app_name = "accounts"

urlpatterns = [
    path("profile/<slug:user_name>/", UserProfile.as_view(), name="profile"),
    path('follow/<slug:user_name>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<slug:user_name>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('followers/<slug:user_name>/', FollowerListView.as_view(), name='followers_list'),
    path('following/<slug:user_name>/', FollowingListView.as_view(), name='following_list'),

]
