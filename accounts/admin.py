from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth')
    list_filter = ('gender',)
    search_fields = ('user__username',)


@admin.register(models.ActivateToken)
class ActivateTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'create_at')
    search_fields = ('user_username', 'user__email')


@admin.register(models.PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'create_at')
    search_fields = ('user_username', 'user__email')


@admin.register(models.APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'create_at')
    search_fields = ('user_username', 'user__email')
