from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "U must to be the owner!"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
