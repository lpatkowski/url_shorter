from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class IsAccountAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        result = super(IsAccountAdminOrReadOnly, self).has_permission(request, view)
        return result or request.method in SAFE_METHODS