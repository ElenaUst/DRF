from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Класс для роли модератора"""
    message = "Доступно только модераторам!"

    def has_permission(self, request, view):
        """Метод для определения принадлежности к группе модераторов"""
        if request.user.groups.filter(name="Moderator").exists():
            return True
        return False


class IsOwner(BasePermission):
    """Класс для роли создателя"""
    message = "Доступно только создателю!"

    def has_object_permission(self, request, view, obj):
        """Метод для проверки принадлежности продукта создателю"""
        if request.user == obj.owner:
            return True
        return False
