from functools import wraps
from django.shortcuts import redirect
from Home.models import SignUp


def login_required_custom(view_func):
    """
    Session-based login guard for the custom SignUp model
    (this project doesn't use Django's built-in auth User model).
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect(f'/Login?next={request.get_full_path()}')
        try:
            request.current_user = SignUp.objects.get(id=user_id)
        except SignUp.DoesNotExist:
            request.session.flush()
            return redirect(f'/Login?next={request.get_full_path()}')
        return view_func(request, *args, **kwargs)
    return wrapper