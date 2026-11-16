"""Admin-only login.
"""
import hmac
import time
from functools import wraps
from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

ADMIN_USERS = {email.lower(): info for email, info in settings.ADMIN_USERS.items()}


def login_required(view):
    """Send visitors who have not signed in to the login page."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_email"):
            return redirect(f"/login/?{urlencode({'next': request.get_full_path()})}")
        return view(request, *args, **kwargs)
    return wrapper


def sign_in(request, email):
    request.session.flush()
    request.session["user_email"] = email
    request.session["user_name"] = ADMIN_USERS[email]["name"]


def password_ok(email, password):
    """True when the password typed matches the one stored for this admin email."""
    stored = ADMIN_USERS[email]["password"]
    return hmac.compare_digest(password.encode(), stored.encode())


def login_view(request):
    if request.session.get("user_email"):
        return redirect("home")

    next_url = request.POST.get("next") or request.GET.get("next") or "/"
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"

    error, notice, problem = None, None, None
    seconds_left = int(request.session.get("locked_until", 0) - time.time())
    step = request.POST.get("step")

    if seconds_left > 0:
        error = "Too many attempts."

    elif request.method == "POST" and step == "restart":
        # "Use a different email" link: go back to the email box.
        request.session.pop("pending_admin", None)

    elif request.method == "POST" and step == "forgot":
        # "Forgot password?" link: email the supervisor, once per visit. Nothing is reset.
        email = request.session.get("pending_admin")
        if email and not request.session.get("help_requested"):
            admin = ADMIN_USERS[email]
            try:
                send_mail(
                    subject=f"Password help needed: {admin['name']}",
                    message=(
                        f"{admin['name']} ({email}) forgot their password.\n\n"
                        "No password was reset. Please contact this agent and "
                        "give them a new password in person.\n\n"
                    ),
                    from_email=None,
                    recipient_list=[settings.SUPERVISOR_EMAIL],
                )
            except Exception:
                error = "The message to your supervisor could not be sent. Contact them directly."
            else:
                request.session["help_requested"] = True
        if email and request.session.get("help_requested"):
            notice = "Your supervisor has been emailed. They will give you a new password in person."

    elif request.method == "POST" and step == "password":
        # Second screen: an admin typing the password.
        email = request.session.get("pending_admin")
        if email and password_ok(email, request.POST.get("password", "")):
            sign_in(request, email)
            return redirect(next_url)
        if email:
            problem = "Wrong password."

    elif request.method == "POST":
        # First screen: the email box.
        email = request.POST.get("email", "").strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            problem = "That doesn't look like an email address."
        else:
            if email in ADMIN_USERS:
                request.session["pending_admin"] = email
            else:
                problem = "That email is not authorized to use this site."

    if problem:
        attempts = request.session.get("failed_attempts", 0) + 1
        remaining = settings.LOGIN_MAX_ATTEMPTS - attempts
        if remaining <= 0:
            request.session["locked_until"] = time.time() + settings.LOGIN_LOCKOUT_SECONDS
            request.session["failed_attempts"] = 0
            error = "Too many attempts."
            seconds_left = settings.LOGIN_LOCKOUT_SECONDS
        else:
            request.session["failed_attempts"] = attempts
            error = f"{problem} {remaining} attempt(s) left."

    pending = request.session.get("pending_admin")
    return render(request, "dashboard/login.html", {
        "error": error,
        "notice": notice,
        "locked": seconds_left > 0,
        "seconds_left": max(seconds_left, 0),
        "max_attempts": settings.LOGIN_MAX_ATTEMPTS,
        "lockout_seconds": settings.LOGIN_LOCKOUT_SECONDS,
        "next": next_url,
        "admin_email": pending,
        "admin_name": ADMIN_USERS[pending]["name"] if pending in ADMIN_USERS else None,
    })


def logout_view(request):
    if request.method == "POST":
        request.session.flush()
    return redirect("login")