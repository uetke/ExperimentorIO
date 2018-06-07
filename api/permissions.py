from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only owners of the endpoint to access it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerSignal(permissions.BasePermission):
    """
    Custom permission to check if the signal belongs to the user requesting
    """
    def has_object_permission(self, request, view, obj):
        return obj.experiment.owner == request.user