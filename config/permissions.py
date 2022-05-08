from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsTeacher(BasePermission):
    """
    Allows access only to teachers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.job == 1)


class IsConfirmedTeacher(BasePermission):
    """
    Allows access only to confirmed teachers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.job == 1 and request.user.confirmed)


class IsStudent(BasePermission):
    """
    Allows access only to students.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.job == 2)
