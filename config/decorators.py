from django.shortcuts import redirect


def non_guest_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        if getattr(user, 'is_guest', False):
            return redirect('/')

        return view_func(request, *args, **kwargs)

    return wrapper