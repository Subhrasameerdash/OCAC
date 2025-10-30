from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("products:product_list")


def register(request: HttpRequest) -> HttpResponse:
    """Handle user registration."""

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("products:product_list")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Simple dashboard placeholder for future profile features."""

    recent_orders = (
        request.user.orders.prefetch_related("items__product").order_by("-created_at")[:5]
    )
    return render(request, "users/dashboard.html", {"orders": recent_orders})
