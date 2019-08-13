from rest_framework import permissions


class IsSafeMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS)


class InPurchase(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(view.action in ('purchase', 'purchase_items'))