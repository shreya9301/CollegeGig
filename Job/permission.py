from django.core.exceptions import PermissionDenied


def user_is_student(function):
    def wrap(request, *args, **kwargs):

        if request.user.role == 'student':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_faculty(function):
    def wrap(request, *args, **kwargs):

        if request.user.role == 'faculty':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return 