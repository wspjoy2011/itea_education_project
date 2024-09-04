from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import FormView

from .forms import RegisterForm, LoginForm, ProfileForm
from . import models
from .services import AccountsEmailNotification

User = get_user_model()


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('blog:post_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in')
            return redirect('blog:post_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            user_token = models.ActivateToken.objects.create(user=user)

        activate_url = (f'{self.request.scheme}://{self.request.get_host()}'
                        f'{reverse("accounts:activate", args=[user.username, user_token.token])}')

        email_service = AccountsEmailNotification()
        email_service.send_activation_email(
            user.email, user.get_full_name(), activate_url
        )

        messages.info(
            self.request,
            'Registration complete. Please check your email.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ActivateAccountView(View):
    def get(self, request, username, token):
        user = get_object_or_404(User, username=username)
        token = get_object_or_404(models.ActivateToken, token=token, user=user)

        if user.is_active:
            token.delete()
            messages.error(request, 'User is already activated')
            return redirect('blog:post_list')

        if token.verify_token():
            with transaction.atomic():
                user.is_active = True
                token.delete()
                user.save()

            messages.success(request, 'Activation complete')
            return redirect('blog:post_list')

        messages.error(request, 'Token expired')
        return redirect('blog:post_list')


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        remember_me = form.cleaned_data.get("remember_me")
        user = authenticate(self.request, email=email, password=password)

        if not user:
            messages.error(self.request, "Invalid login or password")
            return redirect("accounts:login")

        if remember_me:
            self.request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            self.request.session.set_expiry(0)

        login(self.request, user)

        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        next_url = self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
            return iri_to_uri(next_url)
        return self.get_success_url()

    def get_success_url(self):
        return reverse("blog:post_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You're already logged in")
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


class LogoutView(BaseLogoutView):
    next_page = reverse_lazy("blog:post_list")


class ProfileCreateView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'profile'):
            messages.info(self.request, 'You already have profile')
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_list")

    def get(self, request):
        form = ProfileForm()
        context = {'form': form}
        return render(request, 'accounts/profile/create.html', context)

    def post(self, request):
        form = ProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect(self.get_success_url())

        context = {'form': form}
        return render(request, 'accounts/profile/create.html', context)
