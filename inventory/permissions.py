from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    action_role_map = {}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        action = getattr(view, 'action', None)
        allowed_roles = self.action_role_map.get(action, [])
        return bool(request.user.groups.filter(name__in=allowed_roles).exists())


class ProductPermission(RolePermission):
    action_role_map = {
        'list': ['Admin', 'Manager', 'Sales Staff'],
        'retrieve': ['Admin', 'Manager', 'Sales Staff'],
        'create': ['Admin', 'Manager'],
        'update': ['Admin', 'Manager'],
        'partial_update': ['Admin', 'Manager'],
        'destroy': ['Admin'],
    }


class CategoryPermission(RolePermission):
    action_role_map = {
        'list': ['Admin', 'Manager', 'Sales Staff'],
        'retrieve': ['Admin', 'Manager', 'Sales Staff'],
        'create': ['Admin'],
        'update': ['Admin'],
        'partial_update': ['Admin'],
        'destroy': ['Admin'],
    }


class SupplierPermission(RolePermission):
    action_role_map = {
        'list': ['Admin', 'Manager', 'Sales Staff'],
        'retrieve': ['Admin', 'Manager', 'Sales Staff'],
        'create': ['Admin', 'Manager'],
        'update': ['Admin', 'Manager'],
        'partial_update': ['Admin', 'Manager'],
        'destroy': ['Admin', 'Manager'],
    }


class CustomerPermission(RolePermission):
    action_role_map = {
        'list': ['Admin', 'Manager', 'Sales Staff'],
        'retrieve': ['Admin', 'Manager', 'Sales Staff'],
        'create': ['Admin', 'Manager', 'Sales Staff'],
        'update': ['Admin', 'Manager'],
        'partial_update': ['Admin', 'Manager'],
        'destroy': ['Admin'],
    }


class SalePermission(RolePermission):
    action_role_map = {
        'list': ['Admin', 'Manager', 'Sales Staff'],
        'retrieve': ['Admin', 'Manager', 'Sales Staff'],
        'create': ['Admin', 'Manager', 'Sales Staff'],
        'update': ['Admin', 'Manager'],
        'partial_update': ['Admin', 'Manager'],
        'destroy': ['Admin', 'Manager'],
    }
