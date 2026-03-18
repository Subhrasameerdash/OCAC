from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, UpdateView

from .forms import LoginForm, ProfileUpdateForm, SignUpForm

User = get_user_model()


# ── Signup ────────────────────────────────────────────────────────────
class SignUpView(View):
    def get(self, request):
        return render(request, 'accounts/signup.html', {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='accounts.backends.EmailOrUsernameBackend')
            return redirect('feed')
        return render(request, 'accounts/signup.html', {'form': form})


# ── Login ─────────────────────────────────────────────────────────────
class CustomLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('feed')
        return render(request, 'accounts/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username_or_email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user, backend='accounts.backends.EmailOrUsernameBackend')
                return redirect('feed')
            form.add_error(None, 'Invalid username/email or password.')
        return render(request, 'accounts/login.html', {'form': form})


# ── Logout ────────────────────────────────────────────────────────────
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

    def post(self, request):
        logout(request)
        return redirect('login')


# ── Profile (public) ─────────────────────────────────────────────────
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        ctx['posts'] = profile_user.post_set.all()
        ctx['is_following'] = self.request.user.is_following(profile_user)
        return ctx


# ── Profile Edit ──────────────────────────────────────────────────────
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return f'/accounts/profile/{self.request.user.username}/'


# ── Follow / Unfollow (AJAX) ─────────────────────────────────────────
@login_required
def toggle_follow(request, user_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

    if request.user.is_following(target):
        target.followers.remove(request.user)
        following = False
    else:
        target.followers.add(request.user)
        following = True

    return JsonResponse({
        'following': following,
        'follower_count': target.follower_count(),
    })
