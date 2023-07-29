from django.contrib.auth.models import Permission

class IsAuthorOrReadOnlyPermission(Permission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        
        if request.user and request.user.is_authenticated:
            return request.user == view.object.user

        return False

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
