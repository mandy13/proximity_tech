
from rest_framework import permissions
from webapp.models import User


class IsStudent(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        student = User.objects.get(pk=request.user.pk)

        return student.is_student


class IsInstructor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        instructor = User.objects.get(pk=request.user.pk)

        return instructor.is_instructor

    def has_permission(self, request, view):
        instructor = User.objects.get(pk=request.user.pk)

        return instructor.is_instructor


class ListAndRetrieve(permissions.BasePermission):

    def has_permission(self, request, view):
        print("perm", view.action)
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['update', 'create', 'destroy', 'mostviewed']:

            print("returning true")
            instructor = User.objects.get(pk=request.user.pk)

            return instructor.is_instructor
        else:
            return False