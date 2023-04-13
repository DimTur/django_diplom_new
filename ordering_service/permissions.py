from rest_framework.permissions import BasePermission


class IsShopOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.shop.user_id == request.user.id


class IsOrderOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False

# return obj.order.user_id == request.user.id