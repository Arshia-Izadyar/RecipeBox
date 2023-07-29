from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views import View

User = get_user_model()


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if not hasattr(self, "user_object"):
            user_object = User.objects.prefetch_related("following", "recipe", "comments", "likes", "favorites").get(
                username=kwargs.get("user_name")
            )
        
        context["user_is_following"] = user_object.is_following(self.request.user)
        context["user"] = user_object
        context["following"] = user_object.following.all()
        context["recipes"] = user_object.recipe.all()
        context["likes"] = user_object.likes.all()
        context["favorites"] = user_object.favorites.all()
        context["comments"] = user_object.comments.all()
        return context


class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_name = kwargs.get('user_name')
        user_to_follow = get_object_or_404(User, username=user_name)
        request.user.following.add(user_to_follow)
        return redirect('accounts:profile', user_name=user_name)
    
class UnfollowUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_name = kwargs.get('user_name')
        user_to_unfollow = get_object_or_404(User, username=user_name)
        request.user.following.remove(user_to_unfollow)
        return redirect('accounts:profile', user_name=user_name)

class FollowerListView(LoginRequiredMixin, ListView):
    context_object_name = 'followers'
    template_name = "user/followers_list.html"
    
    def get_queryset(self):
        username = self.kwargs['user_name']
        a =User.objects.filter(username=username).first().followers.all()
        print(a)
        return a
    

class FollowingListView(LoginRequiredMixin, ListView):
    context_object_name = 'following'
    template_name = "user/following_list.html"
    
    def get_queryset(self):
        username = self.kwargs['user_name']
        user = User.objects.prefetch_related('following').get(username=username)
        return user.following.all()
    