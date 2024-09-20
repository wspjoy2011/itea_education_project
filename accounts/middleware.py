from django.urls import reverse
from django.shortcuts import redirect


class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        create_profile_url = reverse('accounts:profile_create')
        logout_url = reverse('accounts:logout')
        admin_base_url = '/admin/'

        if request.user.is_authenticated and not hasattr(request.user, 'profile'):
            if not request.path.startswith(admin_base_url) and request.path not in [create_profile_url, logout_url]:
                return redirect(create_profile_url)

        response = self.get_response(request)
        return response
