from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index.html')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            group_count = 0
            if request.user.groups.exists():
                group = request.user.groups.all()
                group_count = group.count()

            item = 0
            if item < group_count:
                if group[item].name in allowed_roles:
                    return view_func(request, *args, **kwargs)
                item += 1
            # return render(request, 'index.html')
            return redirect(request.META.get('HTTP_REFERER'))
        return wrapper_func
    return decorator