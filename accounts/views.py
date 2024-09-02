from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView

from .forms import RegisterForm
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

