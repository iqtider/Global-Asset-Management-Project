"""Demo login: anyone with a correctly formatted email address can sign in.

There is no password and no user table. The email is kept in the session
(a signed browser cookie), and after LOGIN_MAX_ATTEMPTS badly formatted
attempts the form is locked for LOGIN_LOCKOUT_SECONDS.
"""
import time
from functools import wraps
from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme


def login_required(view):
    """Send visitors without an email in their session to the login page."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_email"):
            return redirect(f"/login/?{urlencode({'next': request.get_full_path()})}")
        return view(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.session.get("user_email"):
        return redirect("home")

    next_url = request.POST.get("next") or request.GET.get("next") or "/"
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"

    error = None
    locked_until = request.session.get("locked_until", 0)
    seconds_left = int(locked_until - time.time())

    if seconds_left > 0:
        error = f"Too many attempts. Try again in {seconds_left // 60 + 1} minute(s)."
    elif request.method == "POST":
        email = request.POST.get("email", "").strip()
        try:
            validate_email(email)
        except ValidationError:
            attempts = request.session.get("failed_attempts", 0) + 1
            remaining = settings.LOGIN_MAX_ATTEMPTS - attempts
            if remaining <= 0:
                request.session["locked_until"] = time.time() + settings.LOGIN_LOCKOUT_SECONDS
                request.session["failed_attempts"] = 0
                minutes = settings.LOGIN_LOCKOUT_SECONDS // 60
                error = f"Too many attempts. Try again in {minutes} minute(s)."
                seconds_left = settings.LOGIN_LOCKOUT_SECONDS
            else:
                request.session["failed_attempts"] = attempts
                error = f"That doesn't look like an email address. {remaining} attempt(s) left."
        else:
            request.session.flush()
            request.session["user_email"] = email
            return redirect(next_url)

    return render(request, "dashboard/login.html", {
        "error": error,
        "locked": seconds_left > 0,
        "next": next_url,
    })


def logout_view(request):
    if request.method == "POST":
        request.session.flush()
    return redirect("login")
